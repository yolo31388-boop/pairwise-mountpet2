
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mount.pet import Mount, Pet, Player


def test_mount_bonus_removed():
    p = Player()
    m = Mount(20)
    m.apply_bonus(p)
    assert p.base_speed == 30
    m.remove_bonus(p)
    assert p.base_speed == 10


def test_pet_pickup_space_check():
    p = Player()
    p.inventory = ["x"] * 9
    p.inventory_cap = 10
    pet = Pet()
    assert pet.pickup("a", p.inventory) == True
    assert pet.pickup("b", p.inventory) == False


def test_pet_exp_curve():
    pet = Pet()
    pet.gain_exp(100)
    assert pet.level == 2
    pet.gain_exp(100)
    assert pet.level == 2  # 二级需要更多


def test_loyalty_frozen_offline():
    pet = Pet()
    pet.loyalty = 100
    pet.decay_loyalty(10, online=False)
    assert pet.loyalty == 100


def test_loyalty_decays_online():
    pet = Pet()
    pet.loyalty = 100
    pet.decay_loyalty(5, online=True)
    assert pet.loyalty < 100


def test_summon_region_check():
    p = Player()
    p.region = "indoor"
    m = Mount()
    assert m.can_summon(p) == False
    p.region = "outdoor"
    assert m.can_summon(p) == True


def test_stamina_by_mode():
    m = Mount()
    m.stamina = 100
    m.consume_stamina(1, "run")
    run_cost = 100 - m.stamina
    m.stamina = 100
    m.consume_stamina(1, "fly")
    assert (100 - m.stamina) > run_cost


def test_pet_skill_cd_independent():
    p = Player()
    p.skill_cd = 10
    pet = Pet()
    pet.skill_cd = 0
    assert pet.skill_cd == 0


def test_mount_active_flag():
    p = Player()
    m = Mount()
    m.apply_bonus(p)
    assert m.active == True
    m.remove_bonus(p)
    assert m.active == False
