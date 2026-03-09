import json

# Leer el archivo
with open('enemigos.json', 'r', encoding='utf-8') as f:
    content = f.read()

print(f'File length: {len(content)}')

# Encontrar el primer cierre válido
first_jefes = content.find('"jefes": []')
print(f'First jefes at: {first_jefes}')

if first_jefes > 0:
    # Buscar el segundo "jefes": [] para saber donde empieza el duplicado
    second_jefes = content.find('"jefes": []', first_jefes + 10)
    print(f'Second jefes at: {second_jefes}')
    
    if second_jefes > 0:
        # El contenido válido termina justo antes del segundo bloque duplicado
        # Buscar hacia atrás desde second_jefes para encontrar el cierre correcto
        
        # El patrón correcto termina con: }\n}\n
        # Buscar el último }\n} antes del duplicado
        
        # Retroceder desde second_jefes para encontrar el inicio del duplicado
        # El duplicado empieza con "magicos": []
        
        # Buscar "magicos": [] antes de second_jefes
        first_magicos = content.rfind('"magicos": []', 0, second_jefes)
        print(f'First magicos at: {first_magicos}')
        
        if first_magicos > 0:
            # El contenido válido termina después del primer "jefes": []
            # Buscar el cierre después de first_jefes
            
            # Después de "jefes": [] viene: \n    ]\n  }\n}
            # Buscar el patrón de cierre
            after_jefes = content[first_jefes:first_jefes+50]
            print(f'After first jefes: {repr(after_jefes)}')
            
            # El cierre correcto es: "jefes": []\n    ]\n  }\n}
            # Buscar el ] después de jefes
            close_bracket = content.find(']', first_jefes)
            print(f'Close bracket at: {close_bracket}')
            
            if close_bracket > 0:
                # Buscar el } después del ]
                close_brace1 = content.find('}', close_bracket)
                print(f'Close brace1 at: {close_brace1}')
                
                if close_brace1 > 0:
                    close_brace2 = content.find('}', close_brace1 + 1)
                    print(f'Close brace2 at: {close_brace2}')
                    
                    if close_brace2 > 0:
                        valid_end = close_brace2 + 1
                        valid_content = content[:valid_end]
                        
                        print(f'Valid content length: {len(valid_content)}')
                        print(f'Last 50 chars: {repr(valid_content[-50:])}')
                        
                        try:
                            data = json.loads(valid_content)
                            print(f'Valid JSON!')
                            print(f'Bestias: {len(data["enemigos"]["bestias"])}')
                            print(f'Humanoides: {len(data["enemigos"]["humanoides"])}')
                            
                            # Guardar
                            with open('enemigos.json', 'w', encoding='utf-8') as f:
                                f.write(valid_content)
                            print('File saved!')
                        except json.JSONDecodeError as e:
                            print(f'JSON Error: {e}')
    else:
        print('No duplicate found')
        try:
            data = json.loads(content)
            print('JSON is valid!')
        except json.JSONDecodeError as e:
            print(f'JSON Error: {e}')
