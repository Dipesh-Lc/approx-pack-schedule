from apsuite.scheduling.identical.algorithms import list_scheduling, lpt
from apsuite.scheduling.identical.lower_bounds import lb_makespan_identical

def test_lb_identical_basic():
    p = [3, 3, 3]
    assert lb_makespan_identical(p, m=2) == max(sum(p)/2, 3)

def test_list_scheduling_makespan_ge_lb():
    p = [8, 7, 6, 5, 4]
    m = 2
    sched = list_scheduling(p, m=m)
    lb = lb_makespan_identical(p, m=m)
    assert sched.makespan >= lb - 1e-12

def test_lpt_not_worse_than_list_on_same_instance_often():
    p = [8, 7, 6, 5, 4]
    m = 2
    s1 = list_scheduling(p, m=m)
    s2 = lpt(p, m=m)
    assert s2.makespan <= s1.makespan + 1e-12