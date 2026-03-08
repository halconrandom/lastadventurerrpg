# -*- coding: utf-8 -*-
"""
Tests para la API de exploracion.
"""

import sys
import os

# Configurar path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(backend_dir, 'src'))

import unittest
from flask import Flask

from api.exploracion import exploracion_bp, registrar_blueprint
from systems.seed import init_global_seed


class TestAPIExploracion(unittest.TestCase):
    """Tests para los endpoints de exploracion."""
    
    def setUp(self):
        """Configura la app Flask para testing."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        registrar_blueprint(self.app)
        self.client = self.app.test_client()
        
        # Inicializar semilla
        init_global_seed("test-api-seed")
    
    def test_endpoint_iniciar_exploracion(self):
        """El endpoint /iniciar funciona correctamente."""
        response = self.client.post('/api/exploracion/iniciar', 
            json={'slot': 1, 'x': 0, 'y': 0},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('zona', data['data'])
        self.assertIn('clima', data['data'])
        
        print(f"[OK] Endpoint iniciar: {data['message']}")
    
    def test_endpoint_iniciar_sin_slot(self):
        """El endpoint /iniciar falla sin slot."""
        response = self.client.post('/api/exploracion/iniciar',
            json={'x': 0, 'y': 0},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        
        self.assertFalse(data['success'])
        
        print(f"[OK] Error manejado: {data['message']}")
    
    def test_endpoint_obtener_zona(self):
        """El endpoint /zona/<x>/<y> funciona."""
        # Primero iniciar exploracion para poblar cache
        self.client.post('/api/exploracion/iniciar',
            json={'slot': 1, 'x': 5, 'y': 5},
            content_type='application/json'
        )
        
        # Luego obtener zona
        response = self.client.get('/api/exploracion/zona/5/5?slot=1')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        print(f"[OK] Endpoint zona: zona obtenida")
    
    def test_endpoint_explorar(self):
        """El endpoint /explorar funciona."""
        response = self.client.post('/api/exploracion/explorar',
            json={'slot': 1, 'x': 10, 'y': 10},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('tiles_descubiertos', data['data'])
        
        print(f"[OK] Endpoint explorar: {len(data['data']['tiles_descubiertos'])} tiles")
    
    def test_endpoint_clima(self):
        """El endpoint /clima/<x>/<y> funciona."""
        response = self.client.get('/api/exploracion/clima/0/0?slot=1&hora=12')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertIn('clima', data['data'])
        self.assertIn('ciclo', data['data'])
        self.assertIn('efectos', data['data'])
        
        print(f"[OK] Endpoint clima: {data['data']['clima']['tipo']}")
    
    def test_endpoint_evento(self):
        """El endpoint /evento funciona."""
        response = self.client.get('/api/exploracion/evento?slot=1&x=0&y=0')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('titulo', data['data'])
        
        print(f"[OK] Endpoint evento: {data['data']['titulo']}")
    
    def test_endpoint_resolver_evento(self):
        """El endpoint /evento/resolver funciona."""
        # Primero obtener un evento
        evento_response = self.client.get('/api/exploracion/evento?slot=1&x=0&y=0')
        evento_data = evento_response.get_json()
        
        if evento_data['success']:
            evento_id = evento_data['data']['id']
            
            # Resolver evento
            response = self.client.post('/api/exploracion/evento/resolver',
                json={'evento_id': evento_id, 'opcion': 0},
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            
            self.assertTrue(data['success'])
            self.assertIn('tipo_resultado', data['data'])
            
            print(f"[OK] Endpoint resolver: {data['data']['tipo_resultado']}")
    
    def test_endpoint_seed_post(self):
        """El endpoint POST /seed funciona."""
        response = self.client.post('/api/exploracion/seed',
            json={'seed': 'mi-semilla-personalizada'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertIn('seed', data['data'])
        
        print(f"[OK] Endpoint seed POST: {data['data']['seed'][:20]}...")
    
    def test_endpoint_seed_get(self):
        """El endpoint GET /seed funciona."""
        # Primero establecer seed
        self.client.post('/api/exploracion/seed',
            json={'seed': 'test-seed-get'},
            content_type='application/json'
        )
        
        # Luego obtener
        response = self.client.get('/api/exploracion/seed')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertIn('seed', data['data'])
        
        print(f"[OK] Endpoint seed GET: {data['data']['seed']}")
    
    def test_determinismo_api(self):
        """La API es determinista."""
        # Primera llamada
        response1 = self.client.post('/api/exploracion/iniciar',
            json={'slot': 1, 'x': 20, 'y': 20, 'seed': 'test-determinismo'},
            content_type='application/json'
        )
        data1 = response1.get_json()
        
        # Segunda llamada con misma semilla
        response2 = self.client.post('/api/exploracion/iniciar',
            json={'slot': 2, 'x': 20, 'y': 20, 'seed': 'test-determinismo'},
            content_type='application/json'
        )
        data2 = response2.get_json()
        
        # Mismo nombre de zona
        self.assertEqual(data1['data']['zona']['nombre'], data2['data']['zona']['nombre'])
        
        print(f"[OK] Determinismo API: {data1['data']['zona']['nombre']}")


def run_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*50)
    print("TESTS: API de Exploracion")
    print("="*50 + "\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAPIExploracion)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    if result.wasSuccessful():
        print("TODOS LOS TESTS PASARON")
    else:
        print(f"TESTS FALLIDOS: {len(result.failures)}")
        print(f"ERRORES: {len(result.errors)}")
    print("="*50 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
