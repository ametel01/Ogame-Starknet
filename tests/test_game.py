import pytest
from utils.helpers import (
    assert_equals, update_starknet_block, reset_starknet_block, get_block_timestamp,
    TIME_ELAPS_SIX_HOURS, TIME_ELAPS_ONE_HOUR)
from conftest import user1


@pytest.mark.asyncio
async def test_account(deploy_game_v1):
    (_, _, erc721, metal, crystal, deuterium, user_one) = deploy_game_v1

    # Assert user is the owner of the NFT generated.
    data = await user1.send_transaction(user_one,
                                        erc721.contract_address,
                                        'ownerOf',
                                        [1, 0])
    assert_equals(data.result.response[0], user_one.contract_address)

    # Assert the NFT balance of user is correct.
    data = await user1.send_transaction(user_one,
                                        erc721.contract_address,
                                        'balanceOf',
                                        [user_one.contract_address])
    assert_equals(data.result.response[0], 1)

    # Assert that initial amount of resources ERC20 is tranferred to user.
    data = await user1.send_transaction(user_one,
                                        metal.contract_address,
                                        'balanceOf',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [500*10**18, 0])

    data = await user1.send_transaction(user_one,
                                        crystal.contract_address,
                                        'balanceOf',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [300*10**18, 0])

    data = await user1.send_transaction(user_one,
                                        deuterium.contract_address,
                                        'balanceOf',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [100*10**18, 0])


@pytest.mark.asyncio
async def test_collect_resources(starknet, deploy_game_v1):
    (_, ogame, _, metal, crystal, deuterium, user_one) = deploy_game_v1

    # Assert that the right amount of resources has accrued.
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [500, 300, 100, 0])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [425, 270, 100, 22])

    response = await user1.send_transaction(user_one,
                                            ogame.contract_address,
                                            'metal_upgrade_start',
                                            [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*2)
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'metal_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [371, 255, 100, 11])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'crystal_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*3)
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'crystal_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [326, 237, 100, 0])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*4)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_complete',
                                 [])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [254, 209, 100, 26])

    # User collect resources.
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'collect_resources',
                                 [])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'deuterium_upgrade_start',
                                 [])
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*5)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'deuterium_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [45, 144, 105, 4])
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*205)
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'collect_resources',
                                 [])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [1357, 1018, 542, 4])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'robot_factory_upgrade_start',
                                 [])
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*206)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'robot_factory_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [960, 900, 343, 4])


@pytest.mark.asyncio
async def test_structures_upgrades(starknet, deploy_game_v1):
    (_, ogame, _, _, _, _, user_one, research_lab) = deploy_game_v1

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_structures_levels',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [0, 0, 0, 0, 0, 0])
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*7)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_complete',
                                 [])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_start',
                                 [])

    # Equivalent of 12 hours pass.
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*8)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_complete',
                                 [])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_start',
                                 [])
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*9)
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'solar_plant_upgrade_complete',
                                 [])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'collect_resources',
                                 [])

    # Assert metal mine level is increasead.
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_structures_levels',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [0, 0, 0, 3, 0, 0])
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*25)
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'collect_resources',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [182, 173, 100, 79])
    response = await user1.send_transaction(user_one,
                                            ogame.contract_address,
                                            'metal_upgrade_start',
                                            [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*26)
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'metal_upgrade_complete',
                                 [])
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*27)
    # Assert metal mine level is increasead.
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_structures_levels',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [1, 0, 0, 3, 0, 0])

    response = await user1.send_transaction(user_one,
                                            ogame.contract_address,
                                            'crystal_upgrade_start',
                                            [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*58)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'crystal_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_structures_levels',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [1, 1, 0, 3, 0, 0])
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'collect_resources',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [448, 384, 100, 57])
    response = await user1.send_transaction(user_one,
                                            ogame.contract_address,
                                            'deuterium_upgrade_start',
                                            [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*109)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'deuterium_upgrade_complete',
                                 [])
    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1150)
    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'collect_resources',
                                 [])

    response = await user1.send_transaction(user_one,
                                            ogame.contract_address,
                                            'robot_factory_upgrade_start',
                                            [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1151)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'robot_factory_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_structures_levels',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [1, 1, 1, 3, 1, 0])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [7091, 5034, 2385, 35])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'research_lab_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1152)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'research_lab_upgrade_complete',
                                 [])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_tech_levels',
                                        [1, 0])
    assert_equals(data.result.response, [
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_structures_levels',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [1, 1, 1, 3, 1, 1])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [6894, 4636, 2186, 35])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'energy_tech_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1153)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'energy_tech_upgrade_complete',
                                 [])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'collect_resources',
                                 [])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [10632, 6328, 3032, 35])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_tech_levels',
                                        [1, 0])
    assert_equals(data.result.response, [
                  1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'energy_tech_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1154)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'energy_tech_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [10635, 4730, 2233, 35])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_tech_levels',
                                        [1, 0])
    assert_equals(data.result.response, [
                  1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'computer_tech_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1155)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'computer_tech_upgrade_complete',
                                 [])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [10639, 4332, 1634, 35])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_tech_levels',
                                        [1, 0])
    assert_equals(data.result.response, [
                  1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'laser_tech_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1156)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'laser_tech_upgrade_complete',
                                 [])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [10442, 4234, 1635, 35])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_tech_levels',
                                        [1, 0])
    assert_equals(data.result.response, [
                  1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'research_lab_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1157)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'research_lab_upgrade_complete',
                                 [])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'resources_available',
                                        [user_one.contract_address])
    assert_equals(data.result.response, [10039, 3832, 1834, 35])
    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_tech_levels',
                                        [1, 0])
    assert_equals(data.result.response, [
                  2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'armour_tech_upgrade_start',
                                 [])

    update_starknet_block(
        starknet=starknet, block_timestamp=TIME_ELAPS_ONE_HOUR*1158)

    await user1.send_transaction(user_one,
                                 ogame.contract_address,
                                 'armour_tech_upgrade_complete',
                                 [])
    assert_equals(data.result.response, [10039, 3832, 1834, 35])

    data = await user1.send_transaction(user_one,
                                        ogame.contract_address,
                                        'get_tech_levels',
                                        [1, 0])
    assert_equals(data.result.response, [
                  2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
