## To Export and Populate static table with code base

### Command

```bash
$ py manage_static_table/manage.py <flag>
```

Example to Export

```bash
$ py scripts/manage_static_table --export
```

Example to Populate

```bash
$ py manage_static_table/manage.py --populate
```

Notes: 

1. Static tables to be declared in manage_static_table/manage.py config object


```python # TODO: how to fix this C:\Program Files\PostgreSQL\15\bin?
config = {
    # add the tables in the array to be exported
    'export_tables': ['core_product'],
    ...other poperties
}
```

2. Add postgres path to env usually C:\Program Files\PostgreSQL\<version>\bin


