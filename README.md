# Minecraft Mob Probability Calculator  
*A CS3620 Databases Final Project Proposal*

# Potential Project Name: 
Blockheads

# Team Members:

Ethan Eisnaugle,
Patrick McConnell,
Jayden Dowell


## Project Goals  
- Allow users to create and save custom “mob spawn scenarios,” specifying conditions such as biome, difficulty, armor, held items, and modifiers.  
- Calculate the probability that a specific mob spawns with the exact attributes defined in the scenario, using documented Minecraft spawn rules and equipment chance tables.
- 20+ tables, integrity constraints.
- Provide interactive write actions (account creation, saved scenarios) and data-driven analytical outputs (rare spawn metrics, biome distributions, equipment frequency).  

---

## Key Features  

### Scenario Builder
Users can construct detailed mob spawn scenarios by selecting:  
- Mob type  
- Biome  
- Light level  
- Difficulty setting  
- Armor pieces (helmet, chestplate, leggings, boots)  
- Held items or weapons  
- Mob variants (baby, jockey, etc.)  
- Additional conditional modifiers  

### Probability Engine  
The application computes:  
- **Spawn probability** based on biome-specific mob weights  
- **Equipment probability** based on per-slot item chances  
- **Combined event probability** for an exact mob configuration  
- **Conditional filtering** for biome, time, difficulty, or environmental rules  

### Potential output analytics
The database includes multiple analytical views such as:  
- A rare spawn leaderboard ranking user-created scenarios  
- Biome and difficulty spawn distributions  
- Armor/weapon spawn frequency visualizations  
- HP/Armor stats of said mob
- Probability of mob spawning compared to real world probabilities Ex. Getting struck by lightning (Potentially find a rare probabilities dataset to do this)

---

### Core Entities  
- `user` — application user accounts   
- `mob` — mob definitions (name, category, stats)  
- `biome` — biome definitions and classifications  
- `item` — armor, tools, weapons, and generic items  
- `scenario` — user-created spawn scenarios

### Minecraft Rule Data  
- `mob_spawn_rule` — biome-specific spawn weights and conditions  
- `mob_equipment_chance` — per-slot equipment spawn probabilities  
- `mob_variant` — baby/adult forms, jockeys, and special variants  
- `mob_texture` — texture and asset references  
- `biome_spawn_weight` — normalized spawn weights per biome  
- `dimension` — overworld, nether, end associations  

### Bridge Tables  
- `scenario_item` — items selected for a scenario  
- `scenario_armor_piece` — armor configuration for a scenario  
- `mob_item_applicability` — which items/armor a mob can spawn with  
- `mob_biome_relation` — valid spawn biomes for each mob  

### Analytics & Derived Tables  
- `rare_spawn_leaderboard` — ranking of rare/unique scenarios  
- `spawn_difficulty_distribution` — difficulty-based spawn metrics  
- `mob_equipment_probability` — computed per-slot probabilities  
  
---

### Links to some relevant datasets
- https://github.com/PrismarineJS/minecraft-data/tree/master
