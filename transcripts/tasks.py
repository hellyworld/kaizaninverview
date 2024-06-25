from datetime import datetime

from django.db import transaction

from kaizaninterview.celery import app
from transcripts.models import Entry


@app.task
def do_something_with_entries():
    for entry in Entry.objects.all().select_related("work_interaction").iterator():
        print(entry, entry.work_interaction.title)


@app.task
def do_something_with_entry(entry_id, content):
    with transaction.atomic():
        entry = Entry.objects.select_for_update().get(entry_id)
        entry.content = generate_content(content)
        entry.save()


def generate_content(entry):
    new_content = entry.content + " " + str(datetime.now())
    return new_content


@app.task
def do_something_once():
    print("This is a one-time task.")
