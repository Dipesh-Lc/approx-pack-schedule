from apsuite.scheduling.identical.algorithms import list_scheduling, lpt
from apsuite.scheduling.identical.lower_bounds import lb_makespan_identical

def main():
    p = [8, 7, 6, 5, 4]
    m = 2

    lb = lb_makespan_identical(p, m=m)
    print(f"Jobs: {p}")
    print(f"Machines: {m}")
    print(f"LB = max(sum/m, max) = {lb:.4f}\n")

    for name, alg in [("LIST", list_scheduling), ("LPT", lpt)]:
        sched = alg(p, m=m)
        C = sched.makespan
        ratio = C / lb if lb > 0 else float("nan")
        print(f"{name}: makespan={C:.4f}, ratio_vs_LB={ratio:.4f}")
        print(f"  loads={['%.2f' % x for x in sched.loads]}")
        print(f"  assignment={sched.machines}\n")

if __name__ == "__main__":
    main()