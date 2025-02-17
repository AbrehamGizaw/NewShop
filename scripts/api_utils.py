from rest_framework import serializers
def FormattedResponseData(msg:str="", err:bool=False,  data: dict | list | None = {}):
    data =  {
        "err":err,
        "msg":msg,
        "data":data
    }
    return data

def generate_ts_interface(serializer_class):
    lines = [f"export interface {serializer_class.__name__} {{"]

    for field_name, field in serializer_class().fields.items():
        ts_type = "string" if isinstance(field, serializers.CharField) else "number"
        lines.append(f"  {field_name}: {ts_type};")

    lines.append("}")
    return "\n".join(lines)

