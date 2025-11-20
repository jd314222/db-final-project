# ER Diagram — Minecraft Mob Spawn Probability Database

Below is the relational structure for the biome-based Minecraft mob probability application. This ER diagram description reflects all tables your team will implement and how they connect.

---

## **Entities & Relationships**

### **1. `biome`**

* **biome_id** (PK)
* biome_name

A simple reference table storing Minecraft biomes.

---

### **2. `mob`**

* **mob_id** (PK)
* mob_name
* can_wear_armor (boolean)
* can_hold_items (boolean)
* notes (optional)

Stores all mobs relevant to equipment/spawn probability.

---

### **3. `mob_spawn_rule`**

* **spawn_rule_id** (PK)
* biome_id (FK → biome.biome_id)
* mob_id (FK → mob.mob_id)
* weight
* min_count
* max_count

Defines biome-specific spawn weights for equipment-eligible mobs.

---

### **4. `item`**

* **item_id** (PK)
* item_name
* item_type (armor, weapon, tool)
* slot (helmet, chestplate, leggings, boots, mainhand, offhand)

Represents armor pieces, weapons, and relevant held items.

---

### **5. `mob_equipment_rule`**

* **equip_rule_id** (PK)
* mob_id (FK → mob.mob_id)
* slot (helmet/chest/legs/boots/mainhand/offhand)
* base_equip_chance
* leather_chance
* gold_chance
* chain_chance
* iron_chance
* diamond_chance
* special_rules (JSON/text)

Stores the static Minecraft equipment probabilities per mob.

---

### **6. `mob_equipment_item`** (junction)

* **equip_item_id** (PK)
* equip_rule_id (FK → mob_equipment_rule.equip_rule_id)
* item_id (FK → item.item_id)
* item_probability

Allows each equipment rule to map to one or more possible items.

---

### **7. `calculated_probability`** (optional materialized computation)

* **calc_id** (PK)
* biome_id (FK)
* mob_id (FK)
* description
* probability_value
* computed_at

Used to cache final combined probabilities (spawn × equipment).

---

### **8. `user_account`** (core app user system)

* **user_id** (PK)
* email (UNIQUE)
* password_hash
* created_at

---

### **9. `user_query_log`** (audit table)

* **log_id** (PK)
* user_id (FK → user_account.user_id)
* query_text
* timestamp

Tracks queries such as “chance of full gold zombie in desert.”

---

## **Relationships Summary**

* **biome 1 ────< mob_spawn_rule >──── 1 mob**
* **mob 1 ────< mob_equipment_rule**
* **mob_equipment_rule 1 ────< mob_equipment_item >──── 1 item**
* **user_account 1 ────< user_query_log**
* **calculated_probability** links back to both biome and mob
