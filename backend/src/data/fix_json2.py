import json

with open('enemigos.json', 'r', encoding='utf-8') as f:
    content = f.read()

print(f'File length: {len(content)}')

# Buscar el último enemigo completo
# Buscar el patrón de cierre correcto del lich_menor
last_lich = content.rfind('"id": "lich_menor"')
print(f'Last lich_menor at: {last_lich}')

if last_lich > 0:
    # Buscar el cierre del objeto lich_menor
    # Después de lich_menor viene el lich_guardian que está truncado
    
    # Buscar el cierre del drops del lich_menor
    # El patrón es: } ] } },
    
    # Buscar el primer ] después del último drop completo
    search_area = content[last_lich:]
    
    # Encontrar el patrón: "fragmento_filacteria" ... } ] }
    fragmento_pos = search_area.find('fragmento_filacteria')
    if fragmento_pos > 0:
        # Después de fragmento_filacteria viene: } ] } },
        after = search_area[fragmento_pos:fragmento_pos+100]
        print(f'After fragmento: {repr(after)}')
        
        # El cierre correcto del lich_menor es: } ] }
        # Buscar el ] que cierra drops
        drops_close = search_area.find(']', fragmento_pos)
        if drops_close > 0:
            print(f'Drops close at relative: {drops_close}')
            
            # El contenido válido termina después del cierre del lich_menor
            # Buscar el } que cierra el enemigo
            enemy_close = search_area.find('}', drops_close + 1)
            if enemy_close > 0:
                print(f'Enemy close at relative: {enemy_close}')
                
                # Calcular posición absoluta
                abs_pos = last_lich + enemy_close + 1
                valid_content = content[:abs_pos]
                
                # Agregar cierre del JSON (sin coma extra)
                valid_content += '\n    ],\n    "magicos": [],\n    "demonios": [],\n    "dragones": [],\n    "unicos": [],\n    "jefes": []\n  }\n}'
                
                try:
                    data = json.loads(valid_content)
                    print(f'Valid JSON! No-muertos: {len(data["enemigos"]["no_muertos"])}')
                    
                    with open('enemigos.json', 'w', encoding='utf-8') as f:
                        f.write(valid_content)
                    print('Saved!')
                except json.JSONDecodeError as e:
                    print(f'JSON Error: {e}')
                    print(f'Last 100 chars: {repr(valid_content[-100:])}')
