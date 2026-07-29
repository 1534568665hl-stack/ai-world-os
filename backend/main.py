from core.world_loader import WorldLoader

loader = WorldLoader("./world")

entities = loader.load_all()

print(f"加载实体数量: {len(entities)}")

for entity in entities:
    print(entity["id"], entity["type"])