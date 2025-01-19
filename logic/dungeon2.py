from .requirements import *
from .location import Location
from locations.all import *


class Dungeon2:
    def __init__(self, options, world_setup, r):
        entrance = Location("D2 Entrance", dungeon=2)
        Location(dungeon=2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET, id="bv")  # chest at entrance
        dungeon2_l2 = Location("D2 Left Door", dungeon=2).connect(entrance, AND(KEY2, FOUND(KEY2, 5)), id="bw")  # towards map chest
        dungeon2_map_chest = Location(dungeon=2).add(DungeonChest(0x12E)).connect(dungeon2_l2, AND(r.attack_hookshot_powder, OR(FEATHER, HOOKSHOT)), id="bx")  # map chest
        dungeon2_r2 = Location("D2 After Torches", dungeon=2).connect(entrance, r.fire, id="by")
        Location(dungeon=2).add(DroppedKey(0x132)).connect(dungeon2_r2, r.attack_skeleton, id="bz")
        Location(dungeon=2).add(DungeonChest(0x137)).connect(dungeon2_r2, AND(KEY2, FOUND(KEY2, 5), OR(r.rear_attack, r.rear_attack_range)), id="c0")  # compass chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x133)).connect(dungeon2_r2, STONE_BEAK2, id="c1")
        dungeon2_r3 = Location(dungeon=2).add(DungeonChest(0x138)).connect(dungeon2_r2, r.hit_switch, id="c2")  # first chest with key, can hookshot the switch in previous room
        dungeon2_r4 = Location(dungeon=2).add(DungeonChest(0x139)).connect(dungeon2_r3, FEATHER, id="c3")  # button spawn chest
        if options.logic == "casual":
            shyguy_key_drop = Location(dungeon=2).add(DroppedKey(0x134)).connect(dungeon2_r3, AND(FEATHER, OR(r.rear_attack, r.rear_attack_range)), id="c4")  # shyguy drop key
        else:
            shyguy_key_drop = Location(dungeon=2).add(DroppedKey(0x134)).connect(dungeon2_r3, OR(r.rear_attack, AND(FEATHER, r.rear_attack_range)), id="c5")  # shyguy drop key
        dungeon2_r5 = Location("D2 Pushblock Room", dungeon=2).connect(dungeon2_r4, AND(KEY2, FOUND(KEY2, 3)), id="c6")  # push two blocks together room with owl statue
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x12F)).connect(dungeon2_r5, STONE_BEAK2, id="c7")  # owl statue is before miniboss
        miniboss_room = Location("D2 Miniboss Room", dungeon=2).connect(dungeon2_r5, FEATHER, id="c8")
        miniboss = Location(dungeon=2).add(DungeonChest(0x126)).add(DungeonChest(0x121)).connect(miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[1]], id="c9")  # post hinox
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x129)).connect(miniboss, STONE_BEAK2, id="ca")  # owl statue after the miniboss

        dungeon2_ghosts_room = Location("D2 Boo Buddies Room", dungeon=2).connect(miniboss, AND(KEY2, FOUND(KEY2, 5)), id="cb")
        dungeon2_ghosts_chest = Location(dungeon=2).add(DungeonChest(0x120)).connect(dungeon2_ghosts_room, OR(r.fire, BOW), id="cc")  # bracelet chest
        dungeon2_r6 = Location("D2 After Boo Buddies", dungeon=2).add(DungeonChest(0x122)).connect(miniboss, POWER_BRACELET, id="cd")
        dungeon2_boss_key = Location(dungeon=2).add(DungeonChest(0x127)).connect(dungeon2_r6, AND(r.attack_hookshot_powder, OR(BOW, BOMB, MAGIC_ROD, AND(OCARINA, SONG1), POWER_BRACELET)), id="ce")
        dungeon2_pre_stairs_boss = Location("D2 Before Boss Stairs", dungeon=2).connect(dungeon2_r6, AND(POWER_BRACELET, KEY2, FOUND(KEY2, 5)), id="cf")
        dungeon2_post_stairs_boss = Location("D2 Boss Stairs", dungeon=2).connect(dungeon2_pre_stairs_boss, POWER_BRACELET, id="cg")
        dungeon2_pre_boss = Location("D2 Outside Boss Room", dungeon=2).connect(dungeon2_post_stairs_boss, FEATHER, id="ch")
        # If we can get here, we have everything for the boss. So this is also the goal room.
        dungeon2_boss_room = Location("D2 Boss Room", dungeon=2).connect(dungeon2_pre_boss, NIGHTMARE_KEY2, id="ci")
        dungeon2_boss = Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a)).connect(dungeon2_boss_room, r.boss_requirements[world_setup.boss_mapping[1]], id="cj")
        
        if options.logic == 'glitched' or options.logic == 'hell':
            dungeon2_ghosts_chest.connect(dungeon2_ghosts_room, SWORD, id="ck") # use sword to spawn ghosts on other side of the room so they run away (logically irrelevant because of torches at start)
            dungeon2_r6.connect(miniboss, r.super_jump_feather, id="cl") # superjump to staircase next to hinox. 
            
        if options.logic == 'hell':    
            dungeon2_map_chest.connect(dungeon2_l2, AND(r.attack_hookshot_powder, r.boots_bonk_pit), id="cm") # use boots to jump over the pits
            dungeon2_r4.connect(dungeon2_r3, OR(r.boots_bonk_pit, r.hookshot_spam_pit), id="cn") # can use both pegasus boots bonks or hookshot spam to cross the pit room
            dungeon2_r4.connect(shyguy_key_drop, r.rear_attack_range, one_way=True, id="co") # adjust for alternate requirements for dungeon2_r4
            miniboss_room.connect(dungeon2_r5, r.boots_dash_2d, id="cp") # use boots to dash over the spikes in the 2d section
            dungeon2_pre_stairs_boss.connect(dungeon2_r6, AND(r.hookshot_clip_block, OR(BOW, BOMB, MAGIC_ROD, AND(OCARINA, SONG1)), FOUND(KEY2, 5)), id="cq") # hookshot clip through the pot using both pol's voice
            dungeon2_post_stairs_boss.connect(dungeon2_pre_stairs_boss, OR(BOMB, r.boots_jump), id="cr") # use a bomb to lower the last platform, or boots + feather to cross over top (only relevant in hell logic)
            dungeon2_pre_boss.connect(dungeon2_post_stairs_boss, AND(r.boots_bonk_pit, r.hookshot_spam_pit), id="cs") # boots bonk off bottom wall + hookshot spam across the two 1 tile pits vertically
            
        self.entrance = entrance
        self.final_room = dungeon2_boss


class NoDungeon2:
    def __init__(self, options, world_setup, r):
        entrance = Location("D2 Entrance", dungeon=2)
        Location(dungeon=2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET, id="ct")  # chest at entrance
        Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[1]])
        self.entrance = entrance
