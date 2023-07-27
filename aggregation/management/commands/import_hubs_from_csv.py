import csv
from django.core.management.base import BaseCommand
from aggregation.form import HubForm

class Command(BaseCommand):
    help = ("imports hubs from a local csv file")

    def add_arguments(self, parser):
        parser.add_argument("file_path",nargs=1,type=str)

    def handle(self, *args, **options):
        self.file_path = options["file_path"][0]
        self.prepare()
        self.main()
        self.finalise()

    def prepare(self):
        self.imported_counter = 0
        self.skipped_counter = 0
    
    def main(self):
        self.stdout.write("=== Importing Cars ===")
        
        with open(self.file_path,mode="r") as f:
            reader = csv.DictReader(f)
            for index, row_dict in enumerate(reader):
                form = HubForm(data=row_dict)
                if form.is_valid():
                    form.save
                    self.imported_counter +=1
                else:
                    self.stderr.write(f"Erros importing hubs")
                    self.stderr.write(f"{form.errors.as_json()}\n")

    def finalise(self):
        self.stdout.write(f"--------------\n")
        self.stdout.write(f"Rows imported:{self.imported_counter}\n")
        self.stdout.write(f"Rows skipped:{self.skipped_counter}\n\n")
