import csv
from django.core.management.base import BaseCommand
from orders.models import Order
from datetime import datetime

class Command(BaseCommand):
    help = 'Import orders from TSV file'

    def add_arguments(self, parser):
        parser.add_argument('tsv_file', type=str, help='Path to the TSV file')

    def handle(self, *args, **options):
        tsv_file = options['tsv_file']
        with open(tsv_file, 'r') as file:
            tsv_reader = csv.DictReader(file, delimiter='\t')
            for row in tsv_reader:
                try:
                    Order.objects.create(
                        order_id=row['order_id'],
                        customer_id=row['customer_id'],
                        order_date=datetime.strptime(row['order_date'], '%d-%m-%Y').date(),
                        product_id=row['product_id'],
                        product_name=row['product_name'],
                        product_price=float(row['product_price']),
                        quantity=int(row['quantity'])
                    )
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f'Missing column in TSV: {str(e)}'))
                    self.stdout.write(self.style.ERROR(f'Row data: {row}'))
                    return
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing row: {row}. Error: {str(e)}'))
            self.stdout.write(self.style.SUCCESS('Successfully imported orders'))

        orders = Order.objects.all()[:5]
        self.stdout.write(self.style.SUCCESS(f'First 5 imported orders: {list(orders)}'))