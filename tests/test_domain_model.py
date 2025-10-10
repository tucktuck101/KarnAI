from karnai.model import (
    CardInstance,
    ContinuousEffect,
    Phase,
    Player,
    Stack,
    StackItem,
    Step,
    Target,
    Turn,
    Zones,
)


def test_player_defaults_and_mana():
    p = Player(pid=0, name="P0")
    assert p.life == 40
    p.add_mana("G", 2)
    assert p.mana_pool["G"] == 2
    assert p.spend_mana("G", 1) is True
    assert p.mana_pool["G"] == 1


def test_card_instance_move_and_zone_transfer():
    ci = CardInstance(uid="u1", card_id="c1", owner=0, controller=0, zone="hand")
    z = Zones()
    z.hand[0].append(ci.uid)
    moved = z.transfer(ci.uid, z.hand, z.battlefield, 0)
    assert moved
    ci.move_to("battlefield")
    assert ci.zone == "battlefield"


def test_stack_lifo():
    s = Stack()
    s.push(StackItem(source_uid="u1", controller=0, text="Spell A"))
    s.push(StackItem(source_uid="u2", controller=1, text="Spell B"))
    assert len(s) == 2
    top = s.pop()
    assert top.text == "Spell B" and len(s) == 1


def test_effect_and_turn_enums():
    eff = ContinuousEffect(layer=1, text="+1/+1 until end of turn")
    assert eff.duration == "until_end_of_turn"
    t = Turn()
    assert t.phase == Phase.beginning and t.step == Step.untap and t.active_player == 0


def test_target_selector_shape():
    tgt = Target(selector={"zone": "battlefield", "type": "creature"})
    assert "type" in tgt.selector
