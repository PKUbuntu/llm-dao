
# Used for example of list
sample_list_format = {
    "type": "json_object",
    "schema": {
        "type": "object",
        "$defs": { 
            "A": {
                "type": "object",
                "properties": {
                    "place_name": {"type": "string", "description": "eg: 长城(Great Wall)"},
                    "place_addr": {"type": "string", "description": "Address of the place"},
                    "telephone": {"type": "string", "description": "telephone number, only need 1"}
                },
                "required": ["place_name", "place_addr"],
            }
        },

        "properties": {
            "rules": {
                "items": {
                    "$ref": "#/$defs/A"
                },
                "type": "array"
            }
        },
        "required": ["rules"]
    }
}
