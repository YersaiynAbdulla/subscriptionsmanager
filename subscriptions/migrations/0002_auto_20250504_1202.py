from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('subscriptions', 'Category')
    default_categories = [
        'Развлечения',
        'Образование',
        'Музыка',
        'Спорт',
        'Работа',
        'Продукты',
        'Транспорт',
        'Прочее',
    ]
    for name in default_categories:
        Category.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
