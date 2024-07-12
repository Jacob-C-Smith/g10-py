# Imports
import json

json_indent : int = 4
shader_data : dict = {
    'holdout' : {
        'in'  : { 'transform' : [ { 'model' : 'mat4' } ] },
        'get' : None
    },
    'solid color' : {
        'in'  : { 'transform' : [ { 'model' : 'mat4' } ], 'material' : [ { 'color' : 'vec3' } ] },
        'get' : None
    },
    'texture' : {
        'in' : { 'transform' : [ { 'model' : 'mat4' } ], 'material' : [ { 'texture' : '2D texture' } ] }
    }
}

# Transform 
class Transform:

    # Class data
    location : list 
    rotation : list 
    scale    : list 
    
    # Constructor
    def __init__(self, location : list, rotation : list, scale : list):
        
        # Store the location
        self.location = [ 
            round(location[0], 3),
            round(location[1], 3),
            round(location[2], 3)
        ]
        
        # Rotation 
        self.rotation = [ 
            round(rotation[0], 3),
            round(rotation[1], 3),
            round(rotation[2], 3),
            round(rotation[3], 3)
        ]
        
        # Scale
        self.scale = [ 
            round(scale[0], 3),
            round(scale[1], 3),
            round(scale[2], 3)
        ]

        # Done
        return 

    # Serialize the transform to json text
    def json ( self ) -> str:
        
        # Done
        return str(self)
    
    def get ( self ) -> dict:

        # Initialized data
        transform_data : dict = {
            '$schema'  : 'https://schema.g10.app/transform.json',
            'location' : self.location,
            'rotation' : self.rotation,
            'scale'    : self.scale
        }

        # Done
        return transform_data

    def __str__ ( self ) -> str:

        # Initialized data
        json_text : str = json.dumps( self.get(), indent=json_indent)

        # Done
        return json_text
    
    def write ( self, path : str ):
        
        # Open the file
        with open(path, 'w') as f:

            # Write data to the file
            f.write(self.json())

    @staticmethod
    def read ( path : str ):
        
        # Initialized data
        json_text : str = ""

        # Open the file
        with open(path, 'r') as f:

            # Read the file data to the file
            json_text = f.read()

        # Done
        return Transform.from_json_text(json_text)
            
    @staticmethod
    def from_json_text ( json_text : str ):

        location : list
        rotation : list
        scale    : list

        json_value : dict = json.loads(json_text)

        location = json_value['location']
        rotation = json_value['rotation']
        scale    = json_value['scale']

        # Done
        return Transform(location=location, rotation=rotation, scale=scale)

# Camera
class Camera:

    # Class data
    fov      : float
    near     : float
    far      : float
    target   : list 
    up       : list 
    where    : list 

    def __init__ ( self, view : dict, projection : dict ):

        # Set the FOV
        self.fov = projection['fov']

        # Set the near clip
        self.near = projection['clip']['near']

        # Set the far clip
        self.far = projection['clip']['far']

        # Set the target direction
        self.target = [
            view.target[0],
            view.target[1],
            view.target[2]
        ]

        # Set the up direction
        self.up = [
            view.up[0],
            view.up[1],
            view.up[2]
        ]

        # Set the location
        self.location = [
            view.location[0],
            view.location[1],
            view.location[2]
        ]

        # Done
        return

    # Serialize the camera to json text
    def json ( self ) -> str:
        
        # Done
        return str(self)
    
    def get ( self ) -> dict:

        # Initialized data
        camera_data : dict = {
            '$schema' : 'https://schema.g10.app/camera.json',
            'fov' : self.fov,
            'location' : self.location,
            'orientation' : self.target,
            'clip' : {
                'near' : self.near,
                'far' : self.far
            }
        }

        # Done
        return camera_data

    def __str__ ( self ) -> str:

        # Initialized data
        json_text : str = json.dumps( self.get_transform(), indent=json_indent)

        # Done
        return json_text

# Entity
class Entity:

    # Class data
    transform : Transform 
    shader    : str
    
    # Constructor
    def __init__( self, transform : Transform = None, shader : str = None ):

        # Store the transform
        self.transform = transform

        # Store the shader
        self.shader = shader

        # Done
        return 

    def name_get ( self ) -> str:

        # Get
        return self.name 

    # Serializers
    def json ( self ) -> str:
        
        # Done
        return str(self)

    def get ( self ) -> dict:
        
        # Initialized data
        entity_data : dict = {
            '$schema' : 'https://schema.g10.app/entity.json',
            'transform' : self.transform.get(),
            'shader' : self.shader
        }

        # Done
        return entity_data
    
    def __str__ ( self ) -> str:

        # Uninitialized data
        json_text : str

        # Initialized data
        transform : Transform = self.transform
        shader : str = self.shader

        json_data : dict = {
            '$schema'   : 'https://schema.g10.app/entity.json',
            'shader'    : None if shader is None else shader,
            'transform' : None if transform is None else transform
        }

        # Remove properties with empty values
        json_data = { k:v for (k,v) in json_data.items() if v is not None }

        # Serialize the entity to json
        json_text = json.dumps(json_data, indent=json_indent)

        # Done
        return json_text
    
# Scene
class Scene:

    # Class data
    name     : str
    entities : dict = { }
    cameras  : dict
    lights   : dict

    # Constructor
    def __init__( self, name : str, entities : dict = None, cameras : dict = None, lights : dict = None ):

        # Store the name
        self.name = name

        # Store entities
        for k, v in entities.items():
            self.entities[k] = v
        
        # Done
        return
        
    # Getters
    def name_get ( self ) -> str:

        # Get
        return self.name 

    # Serializers
    def json ( self ) -> str:
        
        # Done
        return str(self)

    def __str__ ( self ) -> str:

        # Uninitialized data
        json_text : str

        # Initialized data
        entities : dict = self.entities

        json_data : dict = {
            '$schema' : 'https://schema.g10.app/scene.json',
            'name' : self.name,
            'entities' : { }
        }

        # Store entities
        for k, v in entities.items():
            json_data['entities'][k] = v.get()

        # Serialize the entity to json
        json_text = json.dumps(json_data, indent=json_indent)

        # Done
        return json_text
    