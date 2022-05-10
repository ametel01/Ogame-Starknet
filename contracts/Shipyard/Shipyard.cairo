%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.math import assert_not_zero
from starkware.starknet.common.syscalls import get_caller_address, get_block_timestamp
from contracts.Shipyard.library import (
    _ogame_address,
    get_available_resources,
    ShipyardQue,
    reset_shipyard_que,
    reset_shipyard_timelock,
    shipyard_upgrade_cost,
    shipyard_timelock,
    ships_qued,
    _cargo_ship_requirements_check,
    _cargo_ship_cost,
    CARGO_SHIP_ID,
)
from contracts.Ogame.IOgame import IOgame
from contracts.utils.constants import TRUE, SHIPYARD_BUILDING_ID
from contracts.utils.Formulas import formulas_buildings_production_time

@constructor
func constructor{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    ogame_address : felt
):
    _ogame_address.write(ogame_address)
    return ()
end

########################################################################################################
#                                   SHIPYARD UPGRADE FUNCTION                                          #
# ######################################################################################################

@external
func _shipyard_upgrade_start{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    caller : felt
) -> (metal : felt, crystal : felt, deuterium : felt, time_unlocked : felt):
    alloc_locals
    assert_not_zero(caller)
    let (ogame_address) = _ogame_address.read()
    let (cue_status) = IOgame.get_buildings_timelock_status(ogame_address, caller)
    let current_timelock = cue_status.lock_end
    with_attr error_message("Building que is busy"):
        assert current_timelock = 0
    end
    let (planet_id) = IOgame.owner_of(ogame_address, caller)
    let (_, _, _, _, robot_factory_level, _, shipyard_level) = IOgame.get_structures_levels(
        ogame_address, caller
    )
    let (metal_available, crystal_available, deuterium_available) = get_available_resources(caller)
    let (metal_required, crystal_required, deuterium_required) = shipyard_upgrade_cost(
        shipyard_level
    )
    with_attr error_message("not enough resources"):
        let (enough_metal) = is_le(metal_required, metal_available)
        assert enough_metal = TRUE
        let (enough_crystal) = is_le(crystal_required, crystal_available)
        assert enough_crystal = TRUE
        let (enough_deuterium) = is_le(deuterium_required, deuterium_available)
        assert enough_deuterium = TRUE
    end
    let (building_time) = formulas_buildings_production_time(
        metal_required, crystal_required, robot_factory_level
    )
    let (time_now) = get_block_timestamp()
    let time_unlocked = time_now + building_time

    return (metal_required, crystal_required, deuterium_required, time_unlocked)
end

@external
func _shipyard_upgrade_complete{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    caller : felt
) -> (success : felt):
    alloc_locals
    let (ogame_address) = _ogame_address.read()
    let (is_qued) = IOgame.is_building_qued(ogame_address, caller, SHIPYARD_BUILDING_ID)
    with_attr error_message("Tried to complete the wrong structure"):
        assert is_qued = TRUE
    end
    let (ogame_address) = _ogame_address.read()
    let (planet_id) = IOgame.owner_of(ogame_address, caller)
    let (cue_details) = IOgame.get_buildings_timelock_status(ogame_address, caller)
    let timelock_end = cue_details.lock_end
    let (time_now) = get_block_timestamp()
    let (waited_enough) = is_le(timelock_end, time_now)
    with_attr error_message("Timelock not yet expired"):
        assert waited_enough = TRUE
    end
    return (TRUE)
end

########################################################################################################
#                                   SHIPS UPGRADE FUNCTION                                             #
# ######################################################################################################

@external
func _cargo_ship_build_start{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    caller : felt, number_of_units : felt
) -> (metal : felt, crystal : felt, deuterium : felt):
    alloc_locals
    assert_not_zero(caller)
    let (que_status) = shipyard_timelock.read(caller)
    let current_timelock = que_status.lock_end
    with_attr error_message("Research lab is busy"):
        assert current_timelock = 0
    end
    let (metal_available, crystal_available, deuterium_available) = get_available_resources(caller)
    let (metal_required, crystal_required, deuterium_required) = _cargo_ship_cost(number_of_units)
    let (requirements_met) = _cargo_ship_requirements_check(caller)
    assert requirements_met = TRUE
    with_attr error_message("not enough resources"):
        let (enough_metal) = is_le(metal_required, metal_available)
        assert enough_metal = TRUE
        let (enough_crystal) = is_le(crystal_required, crystal_available)
        assert enough_crystal = TRUE
        let (enough_deuterium) = is_le(deuterium_required, deuterium_available)
        assert enough_deuterium = TRUE
    end
    let (ogame_address) = _ogame_address.read()
    let (_, _, _, _, _, _, shipyard_level) = IOgame.get_structures_levels(ogame_address, caller)
    let (research_time) = formulas_buildings_production_time(
        metal_required, crystal_required, shipyard_level
    )
    let (time_now) = get_block_timestamp()
    let time_end = time_now + research_time
    let que_details = ShipyardQue(CARGO_SHIP_ID, number_of_units, time_end)
    ships_qued.write(caller, CARGO_SHIP_ID, TRUE)
    shipyard_timelock.write(caller, que_details)
    return (metal_required, crystal_required, deuterium_required)
end

@external
func _cargo_ship_build_complete{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    caller : felt
) -> (number_of_units : felt, success : felt):
    alloc_locals
    tempvar syscall_ptr = syscall_ptr
    let (time_now) = get_block_timestamp()
    let (is_qued) = ships_qued.read(caller, CARGO_SHIP_ID)
    with_attr error_message("Tried to complete the wrong ship"):
        assert is_qued = TRUE
    end
    let (cue_details) = shipyard_timelock.read(caller)
    let timelock_end = cue_details.lock_end
    let (waited_enough) = is_le(timelock_end, time_now)
    with_attr error_message("Timelock not yet expired"):
        assert waited_enough = TRUE
    end
    let units_produced = cue_details.units
    reset_shipyard_timelock(caller)
    reset_shipyard_que(caller, CARGO_SHIP_ID)
    return (units_produced, TRUE)
end
