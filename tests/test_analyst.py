import asyncio
from typing import List

from langfuse.decorators import observe

from dialectical_framework.analyst.thought_mapping import ThoughtMapping
from dialectical_framework.cycle import Cycle
from dialectical_framework.dialectical_component import DialecticalComponent
from dialectical_framework.synthesist.factories.generic_wheel_builder import GenericWheelBuilder
from dialectical_framework.synthesist.factories.two_concepts import TwoConcepts
from dialectical_framework.synthesist.factories.wheel_builder_config import WheelBuilderConfig
from dialectical_framework.wisdom_unit import WisdomUnit

user_message = "Putin started the war, Ukraine will not surrender and will finally win!"

# Examples
example_wu1 = WisdomUnit(
    t_minus=DialecticalComponent.from_str("T1-","Destructive aggression"),
    t=DialecticalComponent.from_str("T1","Putin initiates war"),
    t_plus=DialecticalComponent.from_str("T1+","Strategic power projection"),
    a_plus=DialecticalComponent.from_str("A1+","Mutual understanding"),
    a=DialecticalComponent.from_str("A1","Peace negotiations"),
    a_minus=DialecticalComponent.from_str("A1-","Passive submission"),
)
example_wu2 = WisdomUnit(
    t_minus=DialecticalComponent.from_str("T2-","Endless conflict and destruction"),
    t=DialecticalComponent.from_str("T2","Ukraine resists invasion"),
    t_plus=DialecticalComponent.from_str("T2+","Liberation and sovereignty protected"),
    a_plus=DialecticalComponent.from_str("A2+","Immediate peace achieved"),
    a=DialecticalComponent.from_str("A2","Ukraine surrenders to invasion"),
    a_minus=DialecticalComponent.from_str("A2-","Freedom and independence lost"),
)
example_wu3 = WisdomUnit(
    t_minus=DialecticalComponent.from_str("T3-","Military resources drain rapidly"),
    t=DialecticalComponent.from_str("T3","Russian offensive weakens"),
    t_plus=DialecticalComponent.from_str("T3+","Ukrainian victory approaches"),
    a_plus=DialecticalComponent.from_str("A3+","Strategic military strength maintained"),
    a=DialecticalComponent.from_str("A3","Russian military dominance persists"),
    a_minus=DialecticalComponent.from_str("A3-","Total defeat inevitable"),
)
example_wu4 = WisdomUnit(
    t_minus=DialecticalComponent.from_str("T4-","Vengeance intensifies"),
    t=DialecticalComponent.from_str("T4","Ukrainian victory approaches"),
    t_plus=DialecticalComponent.from_str("T4+","Freedom restored"),
    a_plus=DialecticalComponent.from_str("A4+","Stability maintained"),
    a=DialecticalComponent.from_str("A4","Russian dominance persists"),
    a_minus=DialecticalComponent.from_str("A4-","Oppression deepens"),
)

@observe()
def test_thought_mapping():
    nr_of_thoughts = 3
    reasoner = ThoughtMapping(user_message)
    cycles: List[Cycle] = asyncio.run(reasoner.extract(nr_of_thoughts))
    print("\n")
    for cycle in cycles:
        assert len(cycle.dialectical_components) == nr_of_thoughts
        print(cycle.pretty(skip_dialectical_component_explanation=True))

@observe()
def test_wheel_2():
    wbc = WheelBuilderConfig(component_length=7)
    factory = TwoConcepts()
    wheels = asyncio.run(factory.build(user_message, wbc))
    assert len(wheels[0].wisdom_units) == 2
    print("\n")
    print(wheels[0])

@observe()
def test_wheel_3():
    number_of_thoughts = 3
    wbc = WheelBuilderConfig(component_length=7)
    factory = GenericWheelBuilder(target_wu_count=number_of_thoughts)
    wheels = asyncio.run(factory.build(user_message, wbc))
    assert len(wheels[0].wisdom_units) == number_of_thoughts
    print("\n")
    print("\n\n".join(str(wheel) for wheel in wheels))

@observe()
def test_wheel_4():
    number_of_thoughts = 4
    wbc = WheelBuilderConfig(component_length=7)
    factory = GenericWheelBuilder(target_wu_count=number_of_thoughts)
    wheels = asyncio.run(factory.build(user_message, wbc))
    assert len(wheels[0].wisdom_units) == number_of_thoughts
    print("\n")
    print("\n\n".join(str(wheel) for wheel in wheels))