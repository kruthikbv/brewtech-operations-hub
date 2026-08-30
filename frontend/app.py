from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from api_client.auth_client import AuthClient
from api_client.clients_client import ClientsClient
from api_client.dashboard_client import DashboardClient
from api_client.inventory_client import InventoryClient
from api_client.machines_client import MachinesClient
from api_client.services_client import ServicesClient
from auth.auth_manager import initialize, login, logout
from utils.constants import NAVIGATION
from utils.excel_handler import dataframe_to_excel, validate_columns
from utils.formatters import as_records
from utils.styles import apply_theme, login_header, page_header, sidebar_brand

st.set_page_config(page_title='BrewTech Operations Hub', page_icon='BT', layout='wide')
apply_theme()
initialize()


CHART_COLORS = ['#147d73', '#e66a4e', '#d7a33d', '#315c63', '#80a89f']


def readable(value):
    return str(value).replace('_', ' ').title()


def style_chart(figure, height=340):
    figure.update_layout(
        height=height,
        margin=dict(l=28, r=28, t=62, b=34),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#617070', size=12),
        title_font=dict(family='Manrope', color='#172b2b', size=16),
        legend=dict(orientation='h', yanchor='bottom', y=-0.18, xanchor='left', x=0),
        hoverlabel=dict(bgcolor='#172b2b', font_color='white'),
    )
    figure.update_xaxes(showgrid=False, title=None, linecolor='#dce5e1')
    figure.update_yaxes(gridcolor='#e9efec', title=None, zeroline=False)
    return figure


def run_action(action, success_message):
    try:
        action()
        st.success(success_message)
        st.rerun()
    except Exception as error:
        st.error(str(error))


def render_dashboard(token):
    page_header('Operations overview', 'A live view of client deployments, fleet readiness, service activity, and stock health.', 'Command center')
    client = DashboardClient(token)
    summary = client.summary()
    primary_labels = [('Total clients', 'total_clients'), ('Active clients', 'active_clients'), ('Fleet size', 'total_machines'), ('Available now', 'available_machines')]
    secondary_labels = [('Deployed machines', 'deployed_machines'), ('Machines under service', 'machines_under_service'), ('Low-stock items', 'low_stock_items')]
    for column, (label, key) in zip(st.columns(4), primary_labels):
        column.metric(label, summary.get(key, 0))
    for column, (label, key) in zip(st.columns(3), secondary_labels):
        column.metric(label, summary.get(key, 0))
    machine_status = client.analytics('machine-status')
    service_activity = client.analytics('service-activity')
    inventory = client.analytics('inventory-overview')
    for item in machine_status:
        item['display_status'] = readable(item['status'])
    for item in inventory:
        item['display_category'] = readable(item['category'])
    left, right = st.columns(2)
    status_chart = px.pie(machine_status, names='display_status', values='count', hole=0.62, title='Fleet distribution', color_discrete_sequence=CHART_COLORS)
    status_chart.update_traces(textinfo='percent', marker_line_color='white', marker_line_width=2)
    inventory_chart = px.bar(inventory, x='display_category', y='quantity', title='Inventory by category', color='display_category', color_discrete_sequence=CHART_COLORS)
    inventory_chart.update_layout(showlegend=False)
    inventory_chart.update_xaxes(tickangle=-18, tickfont_size=10)
    left.plotly_chart(style_chart(status_chart), use_container_width=True, config={'displayModeBar': False})
    right.plotly_chart(style_chart(inventory_chart), use_container_width=True, config={'displayModeBar': False})
    service_chart = px.area(service_activity, x='service_date', y='count', markers=True, title='Service activity over time', color_discrete_sequence=['#147d73'])
    service_chart.update_traces(line_width=3, fillcolor='rgba(20,125,115,0.12)')
    st.plotly_chart(style_chart(service_chart, 300), use_container_width=True, config={'displayModeBar': False})
    st.subheader('Recent operational activity')
    st.dataframe(client.recent_activity(), use_container_width=True, hide_index=True)


def render_clients(token):
    page_header('Client directory', 'Search accounts, maintain primary contacts, and manage client availability.', 'Relationships')
    client = ClientsClient(token)
    search_column, status_column = st.columns([3, 1])
    search = search_column.text_input('Search clients', placeholder='Code, name, or contact person')
    status_filter = status_column.selectbox('Status', ['', 'ACTIVE', 'INACTIVE'])
    clients = client.all_clients(search=search, status=status_filter)
    st.dataframe(clients, use_container_width=True, hide_index=True)
    add_tab, edit_tab = st.tabs(['Add client', 'Edit or deactivate'])
    with add_tab:
        with st.form('add-client'):
            code = st.text_input('Client code')
            name = st.text_input('Client name')
            contact = st.text_input('Contact person')
            phone = st.text_input('Phone number')
            email = st.text_input('Email')
            city = st.text_input('City')
            address = st.text_area('Address')
            submitted = st.form_submit_button('Create client')
        if submitted:
            run_action(lambda: client.create({'client_code': code, 'client_name': name, 'contact_person': contact, 'phone_number': phone, 'email': email, 'city': city, 'address': address, 'status': 'ACTIVE'}), 'Client created.')
    with edit_tab:
        if clients:
            selected = st.selectbox('Client', clients, format_func=lambda item: f"{item['client_code']} - {item['client_name']}")
            with st.form('edit-client'):
                name = st.text_input('Client name', selected['client_name'])
                contact = st.text_input('Contact person', selected.get('contact_person', ''))
                city = st.text_input('City', selected.get('city', ''))
                status = st.selectbox('Client status', ['ACTIVE', 'INACTIVE'], index=0 if selected['status'] == 'ACTIVE' else 1)
                save = st.form_submit_button('Save changes')
            if save:
                run_action(lambda: client.update(selected['id'], {'client_name': name, 'contact_person': contact, 'city': city, 'status': status}), 'Client updated.')
            if selected['status'] == 'ACTIVE' and st.button('Deactivate client'):
                run_action(lambda: client.deactivate(selected['id']), 'Client deactivated.')


def render_machines(token):
    page_header('Machine fleet', 'Monitor equipment state, update machine details, and inspect deployment or service history.', 'Fleet control')
    client = MachinesClient(token)
    search_column, status_column = st.columns([3, 1])
    search = search_column.text_input('Search machines', placeholder='Code, model, or serial number')
    status_filter = status_column.selectbox('Status', ['', 'AVAILABLE', 'DEPLOYED', 'UNDER_SERVICE', 'INACTIVE'])
    machines = client.all_machines(search=search, status=status_filter)
    st.dataframe(machines, use_container_width=True, hide_index=True)
    add_tab, edit_tab, history_tab = st.tabs(['Add machine', 'Edit machine', 'History'])
    with add_tab:
        with st.form('add-machine'):
            code = st.text_input('Machine code')
            model = st.text_input('Machine model')
            serial = st.text_input('Serial number')
            purchased = st.date_input('Purchase date')
            submit = st.form_submit_button('Create machine')
        if submit:
            run_action(lambda: client.create({'machine_code': code, 'machine_model': model, 'serial_number': serial, 'purchase_date': purchased.isoformat(), 'status': 'AVAILABLE'}), 'Machine created.')
    with edit_tab:
        if machines:
            selected = st.selectbox('Machine', machines, format_func=lambda item: f"{item['machine_code']} - {item['machine_model']}")
            with st.form('edit-machine'):
                model = st.text_input('Model', selected['machine_model'])
                machine_status = st.selectbox('Machine status', ['AVAILABLE', 'DEPLOYED', 'UNDER_SERVICE', 'INACTIVE'], index=['AVAILABLE', 'DEPLOYED', 'UNDER_SERVICE', 'INACTIVE'].index(selected['status']))
                save = st.form_submit_button('Save machine')
            if save:
                run_action(lambda: client.update(selected['id'], {'machine_model': model, 'status': machine_status}), 'Machine updated.')
    with history_tab:
        if machines:
            history_machine = st.selectbox('History for', machines, key='history-machine', format_func=lambda item: item['machine_code'])
            assignments = client.all_assignments(machine=history_machine['id'])
            services = ServicesClient(token).all_records(machine=history_machine['id'])
            st.caption('Assignment history'); st.dataframe(assignments, use_container_width=True, hide_index=True)
            st.caption('Service history'); st.dataframe(services, use_container_width=True, hide_index=True)


def render_assignments(token):
    page_header('Deployments', 'Coordinate machine placement and returns while preserving a complete assignment history.', 'Field operations')
    machine_client = MachinesClient(token)
    assignments = machine_client.all_assignments()
    st.dataframe(assignments, use_container_width=True, hide_index=True)
    assign_tab, return_tab = st.tabs(['Assign machine', 'Return machine'])
    with assign_tab:
        machines = machine_client.all_machines(status='AVAILABLE')
        clients = ClientsClient(token).all_clients(status='ACTIVE')
        if machines and clients:
            with st.form('assign-machine'):
                machine = st.selectbox('Available machine', machines, format_func=lambda item: item['machine_code'])
                client = st.selectbox('Active client', clients, format_func=lambda item: f"{item['client_code']} - {item['client_name']}")
                assigned_date = st.date_input('Assigned date')
                notes = st.text_area('Notes')
                submit = st.form_submit_button('Assign')
            if submit:
                run_action(lambda: machine_client.assign({'machine_id': machine['id'], 'client_id': client['id'], 'assigned_date': assigned_date.isoformat(), 'notes': notes}), 'Machine assigned.')
        else:
            st.info('An available machine and active client are required.')
    with return_tab:
        active = [item for item in assignments if item['assignment_status'] == 'ACTIVE']
        if active:
            assignment = st.selectbox('Active assignment', active, format_func=lambda item: f"{item['machine_code']} - {item['client_name']}")
            with st.form('return-machine'):
                returned_date = st.date_input('Returned date')
                notes = st.text_area('Return notes')
                submit = st.form_submit_button('Confirm return')
            if submit:
                run_action(lambda: machine_client.return_machine(assignment['id'], {'returned_date': returned_date.isoformat(), 'notes': notes}), 'Machine returned.')


def render_services(token):
    page_header('Service management', 'Schedule maintenance, track work in progress, and protect machine operating states.', 'Technical service')
    client = ServicesClient(token)
    records = client.all_records()
    st.dataframe(records, use_container_width=True, hide_index=True)
    create_tab, update_tab = st.tabs(['Create service record', 'Update status'])
    with create_tab:
        machines = MachinesClient(token).all_machines()
        with st.form('create-service'):
            machine = st.selectbox('Machine', machines, format_func=lambda item: item['machine_code'])
            service_date = st.date_input('Service date')
            service_type = st.selectbox('Service type', ['ROUTINE_SERVICE', 'CLEANING', 'REPAIR', 'INSPECTION'])
            technician = st.text_input('Technician name')
            description = st.text_area('Description')
            service_status = st.selectbox('Initial status', ['SCHEDULED', 'IN_PROGRESS'])
            submit = st.form_submit_button('Create service')
        if submit:
            run_action(lambda: client.create({'machine': machine['id'], 'service_date': service_date.isoformat(), 'service_type': service_type, 'technician_name': technician, 'description': description, 'status': service_status}), 'Service record created.')
    with update_tab:
        editable = [item for item in records if item['status'] not in ('COMPLETED', 'CANCELLED')]
        if editable:
            record = st.selectbox('Service record', editable, format_func=lambda item: f"#{item['id']} - {item['status']}")
            choices = ['SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']
            new_status = st.selectbox('New status', choices, index=choices.index(record['status']))
            if new_status == 'IN_PROGRESS': st.warning('The machine will be marked under service.')
            if st.button('Update service status'):
                run_action(lambda: client.update(record['id'], {'status': new_status}), 'Service status updated.')


def render_inventory(token):
    page_header('Inventory control', 'Track consumables and machine supplies, with low-stock risk surfaced immediately.', 'Stockroom')
    client = InventoryClient(token)
    category = st.selectbox('Category', ['', 'BEVERAGE_INGREDIENT', 'CONSUMABLE', 'MACHINE_SUPPLY', 'CLEANING_SUPPLY', 'OTHER'])
    items = client.all_items(category=category)
    frame = pd.DataFrame(items)
    if not frame.empty and 'is_low_stock' in frame:
        st.dataframe(frame.style.apply(lambda row: ['background-color: #ffe3e3' if row.get('is_low_stock') else '' for _ in row], axis=1), use_container_width=True, hide_index=True)
    add_tab, stock_tab, history_tab = st.tabs(['Add item', 'Stock movement', 'Transaction history'])
    with add_tab:
        with st.form('add-inventory'):
            code = st.text_input('Item code'); name = st.text_input('Item name')
            item_category = st.selectbox('Item category', ['BEVERAGE_INGREDIENT', 'CONSUMABLE', 'MACHINE_SUPPLY', 'CLEANING_SUPPLY', 'OTHER'])
            quantity = st.number_input('Opening quantity', min_value=0.0); unit = st.text_input('Unit'); minimum = st.number_input('Minimum stock', min_value=0.0)
            submit = st.form_submit_button('Create item')
        if submit:
            run_action(lambda: client.create({'item_code': code, 'item_name': name, 'category': item_category, 'current_quantity': quantity, 'unit': unit, 'minimum_stock_level': minimum}), 'Inventory item created.')
    with stock_tab:
        if items:
            item = st.selectbox('Inventory item', items, format_func=lambda value: f"{value['item_code']} - {value['item_name']}")
            movement = st.radio('Movement', ['Stock in', 'Stock out'], horizontal=True)
            amount = st.number_input('Quantity', min_value=0.01, value=1.0); remarks = st.text_input('Remarks')
            if st.button('Record movement'):
                operation = client.stock_in if movement == 'Stock in' else client.stock_out
                run_action(lambda: operation(item['id'], {'quantity': amount, 'remarks': remarks}), 'Stock movement recorded.')
    with history_tab:
        if items:
            item = st.selectbox('Transactions for', items, key='transaction-item', format_func=lambda value: value['item_code'])
            st.dataframe(as_records(client.transactions(item['id'])), use_container_width=True, hide_index=True)


def render_analytics(token):
    page_header('Operational analytics', 'Compare fleet utilization, client deployments, service cadence, and inventory position.', 'Performance')
    client = DashboardClient(token)
    machine_status = client.analytics('machine-status')
    machines_per_client = client.analytics('machines-per-client')
    service_activity = client.analytics('service-activity')
    inventory = client.analytics('inventory-overview')
    for item in machine_status:
        item['display_status'] = readable(item['status'])
    for item in inventory:
        item['display_category'] = readable(item['category'])
    top_left, top_right = st.columns(2)
    status_chart = px.pie(machine_status, names='display_status', values='count', hole=0.58, title='Machine status distribution', color_discrete_sequence=CHART_COLORS)
    client_chart = px.bar(machines_per_client, x='client_name', y='count', title='Active machines per client', color_discrete_sequence=['#147d73'])
    top_left.plotly_chart(style_chart(status_chart), use_container_width=True, config={'displayModeBar': False})
    top_right.plotly_chart(style_chart(client_chart), use_container_width=True, config={'displayModeBar': False})
    service_chart = px.line(service_activity, x='service_date', y='count', markers=True, title='Service activity', color_discrete_sequence=['#e66a4e'])
    service_chart.update_traces(line_width=3)
    inventory_chart = px.bar(inventory, x='display_category', y='quantity', title='Current inventory by category', color='display_category', color_discrete_sequence=CHART_COLORS)
    inventory_chart.update_layout(showlegend=False)
    inventory_chart.update_xaxes(tickangle=-18, tickfont_size=10)
    bottom_left, bottom_right = st.columns(2)
    bottom_left.plotly_chart(style_chart(service_chart), use_container_width=True, config={'displayModeBar': False})
    bottom_right.plotly_chart(style_chart(inventory_chart), use_container_width=True, config={'displayModeBar': False})


def render_data_management(token):
    page_header('Data management', 'Validate spreadsheet imports and export clean operational datasets for analysis.', 'Exchange')
    dataset = st.selectbox('Dataset', ['Clients', 'Machines', 'Inventory Items'])
    configurations = {
        'Clients': (['client_code', 'client_name', 'contact_person', 'phone_number', 'email', 'address', 'city', 'status'], ClientsClient(token).create),
        'Machines': (['machine_code', 'machine_model', 'serial_number', 'purchase_date', 'status'], MachinesClient(token).create),
        'Inventory Items': (['item_code', 'item_name', 'category', 'current_quantity', 'unit', 'minimum_stock_level'], InventoryClient(token).create),
    }
    required, create = configurations[dataset]
    uploaded = st.file_uploader('Upload Excel file', type=['xlsx'], key=dataset)
    if uploaded:
        frame = pd.read_excel(uploaded)
        missing = validate_columns(frame, required)
        duplicates = frame.duplicated(subset=[required[0]]).any() if not missing else False
        if missing: st.error(f"Missing columns: {', '.join(missing)}")
        elif duplicates: st.error(f'Duplicate {required[0]} values found.')
        elif dataset == 'Machines' and not set(frame['status']).issubset({'AVAILABLE', 'INACTIVE'}): st.error('Imported machines may only be AVAILABLE or INACTIVE.')
        else:
            st.dataframe(frame, use_container_width=True, hide_index=True)
            confirmed = st.checkbox('I reviewed this import')
            if st.button('Import rows', disabled=not confirmed):
                errors = []
                for row_number, row in frame.iterrows():
                    try:
                        payload = {column: (row[column].isoformat() if hasattr(row[column], 'isoformat') else row[column]) for column in required}
                        create(payload)
                    except Exception as error:
                        errors.append(f'Row {row_number + 2}: {error}')
                if errors: st.error('\n'.join(errors))
                else: st.success(f'Imported {len(frame)} rows.')
    st.divider()
    export_name = st.selectbox('Export dataset', ['Clients', 'Machines', 'Assignments', 'Service Records', 'Inventory', 'Inventory Transactions'])
    if export_name == 'Clients': export_rows = ClientsClient(token).all_clients()
    elif export_name == 'Machines': export_rows = MachinesClient(token).all_machines()
    elif export_name == 'Assignments': export_rows = MachinesClient(token).all_assignments()
    elif export_name == 'Service Records': export_rows = ServicesClient(token).all_records()
    elif export_name == 'Inventory': export_rows = InventoryClient(token).all_items()
    else:
        inventory_client = InventoryClient(token); export_rows = []
        for item in inventory_client.all_items(): export_rows.extend(as_records(inventory_client.transactions(item['id'])))
    st.download_button('Download Excel', dataframe_to_excel(pd.DataFrame(export_rows)), f"{export_name.lower().replace(' ', '_')}.xlsx")


if not st.session_state.is_authenticated:
    login_header()
    with st.form('login'):
        username = st.text_input('Username', placeholder='Enter your username')
        password = st.text_input('Password', type='password', placeholder='Enter your password')
        submitted = st.form_submit_button('Sign in', use_container_width=True)
    if submitted:
        try:
            auth = AuthClient(); tokens = auth.login(username, password)
            login(tokens, AuthClient(tokens['access']).me()); st.rerun()
        except Exception as error:
            st.error(str(error))
    st.stop()

with st.sidebar:
    sidebar_brand(st.session_state.current_user.get('username', ''))
    page = st.radio('Workspace', NAVIGATION, label_visibility='collapsed')
    if st.button('Sign out', use_container_width=True):
        logout(); st.rerun()

renderers = {'Dashboard': render_dashboard, 'Clients': render_clients, 'Machines': render_machines, 'Assignments': render_assignments, 'Service Management': render_services, 'Inventory': render_inventory, 'Analytics': render_analytics, 'Data Management': render_data_management}
try:
    renderers[page](st.session_state.access_token)
except Exception as error:
    st.error(str(error))
