##########################################################################################
#                                               Structs                                  #
##########################################################################################

# @dev Stores the levels of the mines.
struct MineLevels:
    member metal : felt
    member crystal : felt
    member deuterium : felt
end

# @dev Stores the energy available.
struct Energy:
    member solar_plant : felt
    # member satellites : felt
end

# @dev Stores the level of the facilities.
struct Facilities:
    member robot_factory : felt
end

# @dev The main planet struct.
struct Planet:
    member mines : MineLevels
    member energy : Energy
    member facilities : Facilities
    member timer : felt
end

# @dev Used to handle costs.
struct Cost:
    member metal : felt
    member crystal : felt
    member deuterium : felt
end

# @dev Used to represent the civil ships.
struct CivilShips:
    member cargo : felt
    member recycler : felt
    member espyonage_probe : felt
    member solar_satellite : felt
end

# @dev Used to represent the combat ships.
struct CombatShips:
    member light_fighter : felt
    member heavy_fighter : felt
    member cruiser : felt
    member battle_ship : felt
    member death_star : felt
end

# @dev Temporary struct to represent a fleet.
struct Fleet:
    member civil : CivilShips
    member combat : CombatShips
end

# @dev Stores the building on cue details
struct BuildingQue:
    member id : felt
    member lock_end : felt
end

struct TechLevels:
    member research_lab : felt
    member energy_tech : felt
    member computer_tech : felt
    member laser_tech : felt
    member armour_tech : felt
    member ion_tech : felt
    member espionage_tech : felt
    member plasma_tech : felt
    member weapons_tech : felt
    member shielding_tech : felt
    member hyperspace_tech : felt
    member astrophysics : felt
    member comustion_drive : felt
    member hyperspace_drive : felt
    member impulse_drive : felt
end
