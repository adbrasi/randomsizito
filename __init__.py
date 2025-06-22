import random
import re

class RandomResolutionNode:
    """
    ComfyUI Custom Node para gerar resoluções aleatórias com pesos
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "resolutions_text": ("STRING", {
                    "multiline": True,
                    "default": "768x1344:5\n832x1216\n896x1152\n1024x1024\n1024x1536\n1152x896\n1216x832\n1344x768\n1536x1024"
                }),
                "invert": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Width/Height Invertido",
                    "label_off": "Width/Height Normal"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                })
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution_info")
    FUNCTION = "get_random_resolution"
    CATEGORY = "Utils"
    
    def parse_resolutions(self, text):
        """
        Parse do texto de resoluções no formato "WIDTHxHEIGHT:PESO"
        """
        resolutions = []
        weights = []
        
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Regex para capturar resolução e peso opcional
            match = re.match(r'(\d+)x(\d+)(?::(\d+))?', line)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
                weight = int(match.group(3)) if match.group(3) else 1
                
                resolutions.append((width, height))
                weights.append(weight)
        
        return resolutions, weights
    
    def get_random_resolution(self, resolutions_text, invert, seed):
        """
        Seleciona uma resolução aleatória baseada nos pesos
        """
        # Define seed para reprodutibilidade
        random.seed(seed)
        
        # Parse das resoluções
        resolutions, weights = self.parse_resolutions(resolutions_text)
        
        if not resolutions:
            # Fallback para resolução padrão se não conseguir fazer parse
            width, height = 1024, 1024
            resolution_info = "1024x1024 (fallback)"
        else:
            # Seleção ponderada
            selected_resolution = random.choices(resolutions, weights=weights, k=1)[0]
            width, height = selected_resolution
            
            # Informação sobre a resolução selecionada
            resolution_info = f"{width}x{height}"
        
        # Aplicar inversão se solicitada
        if invert:
            width, height = height, width
            resolution_info += " (invertido)"
        
        return width, height, resolution_info

# Dicionário de mapeamento de nodes para ComfyUI
NODE_CLASS_MAPPINGS = {
    "RandomResolutionNode": RandomResolutionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomResolutionNode": "Random Resolution"
}

# Exemplo de uso (para teste):
if __name__ == "__main__":
    node = RandomResolutionNode()
    
    test_text = """768x1344:5
832x1216
896x1152
1024x1024:7
1024x1536
1152x896
1216x832
1344x768
1536x1024"""
    
    # Teste sem inversão
    print("Teste sem inversão:")
    for i in range(10):
        w, h, info = node.get_random_resolution(test_text, False, i)
        print(f"Seed {i}: {w}x{h} - {info}")
    
    print("\nTeste com inversão:")
    for i in range(5):
        w, h, info = node.get_random_resolution(test_text, True, i)
        print(f"Seed {i}: {w}x{h} - {info}")