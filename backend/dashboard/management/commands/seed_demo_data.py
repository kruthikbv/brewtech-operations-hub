from datetime import date, datetime, time, timedelta

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from clients.models import Client
from inventory.models import InventoryItem, InventoryTransaction
from machines.models import Machine, MachineAssignment
from service_records.models import ServiceRecord
from common.constants import CLIENT_ACTIVE, MACHINE_AVAILABLE

class Command(BaseCommand):
    help = 'Create repeatable synthetic BrewTech demonstration data.'

    @staticmethod
    def timestamp(value):
        return timezone.make_aware(datetime.combine(value, time(hour=9)))

    @transaction.atomic
    def handle(self, *args, **options):
        user, created = get_user_model().objects.get_or_create(username='demo_admin', defaults={'email': 'demo@example.test', 'is_staff': True})
        if created: user.set_password('demo-password'); user.save()

        legacy_machines = Machine.objects.filter(machine_code__startswith='DEMO-MCH-')
        legacy_items = InventoryItem.objects.filter(item_code__startswith='DEMO-INV-')
        ServiceRecord.objects.filter(machine__in=legacy_machines).delete()
        MachineAssignment.objects.filter(machine__in=legacy_machines).delete()
        InventoryTransaction.objects.filter(inventory_item__in=legacy_items).delete()
        legacy_machines.delete()
        legacy_items.delete()
        Client.objects.filter(client_code__startswith='DEMO-CLT-').delete()

        client_data = [
            ('Namma Filter House', 'Ananya Rao', 'Indiranagar', '12th Main, Indiranagar, Bengaluru'),
            ('Kaveri Workspaces', 'Karthik Iyer', 'Koramangala', '5th Block, Koramangala, Bengaluru'),
            ('Malabar Bean Collective', 'Nikhil Nair', 'Whitefield', 'ITPL Main Road, Whitefield, Bengaluru'),
            ('Deccan Design Studio', 'Meera Reddy', 'Jayanagar', '4th Block, Jayanagar, Bengaluru'),
            ('Nilgiri Pantry Services', 'Arjun Menon', 'HSR Layout', 'Sector 2, HSR Layout, Bengaluru'),
            ('Udupi Office Kitchens', 'Pooja Shetty', 'Malleshwaram', 'Sampige Road, Malleshwaram, Bengaluru'),
            ('Cauvery Tech Commons', 'Vignesh Kumar', 'Electronic City', 'Neeladri Road, Electronic City, Bengaluru'),
            ('Mysuru Meeting Rooms', 'Kavya Gowda', 'Rajajinagar', 'Dr Rajkumar Road, Rajajinagar, Bengaluru'),
            ('Coastal Brew Canteen', 'Rohan Pai', 'Marathahalli', 'Outer Ring Road, Marathahalli, Bengaluru'),
            ('Thanjavur Corporate Dining', 'Divya Krishnan', 'Bellandur', 'Green Glen Layout, Bellandur, Bengaluru'),
            ('Palakkad Business Centre', 'Adithya Pillai', 'Hebbal', 'Bellary Road, Hebbal, Bengaluru'),
            ('Madurai Desk Cafe', 'Lakshmi Narayanan', 'JP Nagar', '7th Phase, JP Nagar, Bengaluru'),
            ('Tungabhadra Shared Offices', 'Sahana Hegde', 'Yelahanka', 'New Town Main Road, Yelahanka, Bengaluru'),
            ('Chennai Coffee Corner', 'Surya Prakash', 'Banashankari', '3rd Stage, Banashankari, Bengaluru'),
            ('Godavari Workplace Foods', 'Harini Subramanian', 'Domlur', 'Intermediate Ring Road, Domlur, Bengaluru'),
        ]
        clients = []
        for index, (name, contact, city, address) in enumerate(client_data, start=1):
            client, _ = Client.objects.update_or_create(
                client_code=f'CLT-{index:04d}',
                defaults={
                    'client_name': name,
                    'contact_person': contact,
                    'phone_number': f'080-5550-{1000 + index}',
                    'email': f'operations{index}@brewtech-demo.example',
                    'address': address,
                    'city': city,
                    'status': CLIENT_ACTIVE,
                },
            )
            created_date = date(2023, 12, 1) + timedelta(days=index)
            Client.objects.filter(pk=client.pk).update(created_at=self.timestamp(created_date), updated_at=self.timestamp(created_date))
            clients.append(client)

        machine_models = ['Astra Duo Espresso', 'Kaveri Bean-to-Cup', 'Malabar Compact Pro', 'Deccan Office Brew']
        machines = []
        for index in range(1, 41):
            machine, _ = Machine.objects.update_or_create(
                machine_code=f'MCH-{index:04d}',
                defaults={
                    'machine_model': machine_models[(index - 1) % len(machine_models)],
                    'serial_number': f'BT24-KA-{index:05d}',
                    'purchase_date': date(2023, 12, 2) + timedelta(days=(index - 1) * 8),
                    'status': MACHINE_AVAILABLE,
                },
            )
            Machine.objects.filter(pk=machine.pk).update(created_at=self.timestamp(machine.purchase_date), updated_at=self.timestamp(machine.purchase_date))
            machines.append(machine)

        MachineAssignment.objects.filter(machine__machine_code__in=[machine.machine_code for machine in machines]).delete()
        for index in range(20):
            assigned_date = date(2024, 6, 3) + timedelta(days=index * 7)
            assignment = MachineAssignment.objects.create(machine=machines[index], client=clients[index % len(clients)], assigned_date=assigned_date, assignment_status='ACTIVE', notes='Office beverage station deployment')
            MachineAssignment.objects.filter(pk=assignment.pk).update(created_at=self.timestamp(assigned_date), updated_at=self.timestamp(assigned_date))
            machines[index].status = 'DEPLOYED'; machines[index].save(update_fields=['status', 'updated_at'])
            Machine.objects.filter(pk=machines[index].pk).update(updated_at=self.timestamp(assigned_date))
        for index in range(20, 30):
            assigned = date(2023, 12, 11) + timedelta(days=(index - 20) * 14)
            returned = assigned + timedelta(days=75)
            assignment = MachineAssignment.objects.create(machine=machines[index], client=clients[index % len(clients)], assigned_date=assigned, returned_date=returned, assignment_status='RETURNED', notes='Completed workplace refresh deployment')
            MachineAssignment.objects.filter(pk=assignment.pk).update(created_at=self.timestamp(assigned), updated_at=self.timestamp(returned))

        ServiceRecord.objects.filter(machine__in=machines).delete()
        service_types = ['ROUTINE_SERVICE', 'CLEANING', 'REPAIR', 'INSPECTION']
        technicians = ['Pradeep Kumar', 'Sneha Murthy', 'Faisal Rahman', 'Deepak Nair', 'Revathi Shankar']
        service_descriptions = ['Quarterly preventive maintenance', 'Brewing group deep cleaning', 'Pump pressure calibration', 'Water filter and seal inspection']
        for index in range(25):
            service_date = date(2023, 12, 10) + timedelta(days=index * 13)
            record = ServiceRecord.objects.create(machine=machines[index % len(machines)], service_date=service_date, service_type=service_types[index % len(service_types)], technician_name=technicians[index % len(technicians)], description=service_descriptions[index % len(service_descriptions)], status='COMPLETED', previous_machine_status=machines[index % len(machines)].status)
            ServiceRecord.objects.filter(pk=record.pk).update(created_at=self.timestamp(service_date), updated_at=self.timestamp(service_date))

        item_data = [
            ('Arabica House Blend', 'BEVERAGE_INGREDIENT', 'kg', 28, 10),
            ('Chicory Filter Blend', 'BEVERAGE_INGREDIENT', 'kg', 18, 8),
            ('Dairy Whitener', 'BEVERAGE_INGREDIENT', 'kg', 12, 6),
            ('Brown Sugar Sachets', 'CONSUMABLE', 'box', 45, 15),
            ('Compostable Cups 180ml', 'CONSUMABLE', 'sleeve', 9, 12),
            ('Wooden Stirrers', 'CONSUMABLE', 'box', 30, 10),
            ('Espresso Group Gasket', 'MACHINE_SUPPLY', 'piece', 14, 5),
            ('Water Filter Cartridge', 'MACHINE_SUPPLY', 'piece', 7, 8),
            ('Steam Wand Nozzle', 'MACHINE_SUPPLY', 'piece', 10, 4),
            ('Food-safe Descaler', 'CLEANING_SUPPLY', 'bottle', 16, 6),
            ('Backflush Cleaning Tablets', 'CLEANING_SUPPLY', 'jar', 5, 7),
            ('Microfibre Cleaning Cloths', 'CLEANING_SUPPLY', 'pack', 24, 8),
            ('Drip Tray Liners', 'OTHER', 'pack', 20, 6),
            ('Machine ID Labels', 'OTHER', 'sheet', 15, 5),
            ('Service Tool Kit Refills', 'OTHER', 'kit', 3, 4),
        ]
        items = []
        for index, (name, category, unit, quantity, minimum) in enumerate(item_data, start=1):
            item, _ = InventoryItem.objects.update_or_create(item_code=f'INV-{index:04d}', defaults={'item_name': name, 'category': category, 'current_quantity': quantity, 'unit': unit, 'minimum_stock_level': minimum})
            stocked_date = date(2023, 12, 3) + timedelta(days=index)
            InventoryItem.objects.filter(pk=item.pk).update(created_at=self.timestamp(stocked_date), updated_at=self.timestamp(stocked_date))
            items.append(item)

        InventoryTransaction.objects.filter(inventory_item__in=items).delete()
        for index in range(50):
            transaction_type = 'STOCK_IN' if index % 3 != 2 else 'STOCK_OUT'
            transaction_date = date(2023, 12, 5) + timedelta(days=index * 6)
            inventory_transaction = InventoryTransaction.objects.create(inventory_item=items[index % len(items)], transaction_type=transaction_type, quantity=5 if transaction_type == 'STOCK_IN' else 2, transaction_date=transaction_date, remarks='Scheduled warehouse receipt' if transaction_type == 'STOCK_IN' else 'Issued to Bengaluru service route')
            InventoryTransaction.objects.filter(pk=inventory_transaction.pk).update(created_at=self.timestamp(transaction_date))

        self.stdout.write(self.style.SUCCESS('Realistic fictional demo data is ready for December 2023 through October 2024.'))
