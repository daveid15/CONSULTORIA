class DefaultLoader:
    def __init__(self, manifest_file, output_dir, cache=False):
        self.manifest_file = manifest_file
        self.output_dir = output_dir
        self.cache = cache
        self.manifest_data = None

    def get_manifest_data(self):
        # Aquí implementarías la lógica para cargar y procesar el archivo de manifiesto
        # Puede ser leer un archivo JSON, consultar una base de datos, etc.
        # Por simplicidad, asumiremos que es un diccionario con las rutas de los archivos

        if self.cache and self.manifest_data is not None:
            return self.manifest_data
        
        # Ejemplo de carga de un archivo JSON como manifiesto
        import json
        with open(self.manifest_file, 'r') as f:
            self.manifest_data = json.load(f)

        return self.manifest_data

    def get_file_path(self, file_name):
        manifest_data = self.get_manifest_data()
        return manifest_data.get(file_name, file_name)