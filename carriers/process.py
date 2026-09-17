"""Generated atlas section. Maps we run here. Not terrain."""

CARRIERS = [
 dict(id=86, key="PROC_PAIR", name="Process calc pairs",
  origin="studio process-calc / workbook module 4",
  V="Q-pairs (v, r)",
  G="isolate; Leibniz mix; rate = top.r / bottom.r",
  theta="dead isolator r=0 refuses; divisor v=0 refuses",
  outside="Inf, limits, unary D as a property of f, unlistable R",
  insight=("A rate is a ratio of two channels under one cut. Five + * / "
           "on Q send x^2 at 3 to 6. The school path uses five ops and "
           "lands on 6+h. Deleting h is not an op on Q."),
  forces=[
   dict(claim="rate(x*x,x) at 3 is 6 for seeds 1,2,1/2,10,1/3",
        check="proc_gauge_six"),
   dict(claim="pair path is 5 arithmetic ops to 6; school path 5 ops to 6+h",
        check="proc_ops_tape")],
  breaks=[
   dict(claim="rate against r=0 refuses", check="proc_dead_isolator"),
   dict(claim="(9,6) is both x^2 seed 1 and 3x seed 2 — pair is not a receipt",
        check="proc_collision")],
  useful_for=["calc pedagogy", "automatic differentiation reading"]),

 dict(id=87, key="ORIGIN_WRAP", name="Origin wrap (mechanism arithmetic)",
  origin="mathoflogic/origin rebuild",
  V="distinguishable phases of Closure(n)",
  G="co_propagate (a+b)%n ; iterate",
  theta="returns to itself",
  outside="host-free addition; unbounded Nat without a schema",
  insight=("The wrap IS Z/n. Integers are refuse-to-close. co_propagate "
           "uses host + and %. Mechanism reads a wrap; it does not birth +."),
  forces=[
   dict(claim="wrap + agrees with Peano + on {0..8}^2",
        check="origin_routes_add81")],
  breaks=[
   dict(claim="5 reads differently at n=3,7,12",
        check="origin_numeral_split"),
   dict(claim="intruder chain is not reached from 0 by S",
        check="origin_intruder")],
  useful_for=["arithmetic origin", "reification of numerals"]),

 dict(id=88, key="MODUS_MP", name="Detachment as designation-closure",
  origin="mathoflogic/modus",
  V="nine logic carriers (CL2,K3,LP,L3+,...)",
  G="MP / MT on designated set",
  theta="designated values",
  outside="MP as a law of thought; a token of the rule sitting in V",
  insight=("Detachment dies where the glut is designated. K3 gap protects. "
           "POST4 can be valid and meaningless. G is not a token in V."),
  forces=[
   dict(claim="CL2 and K3 keep MP on the full table", check="modus_k3_mp"),
   dict(claim="LP loses MP at (1/2,0)", check="modus_lp_mp_dies")],
  breaks=[
   dict(claim="reifying MP as a premise does not detach B (Carroll shape)",
        check="modus_tortoise")],
  useful_for=["inference engines", "sorites metering"]),

 dict(id=89, key="MODAL_ATLAS", name="Modal frames generated n<=3",
  origin="studio/modal + carriersets/modal, recount",
  V="listed W, listed R, atoms p,q",
  G="BOX=all successors DIA=any; filters on R",
  theta="valid on every world of every passing frame under every val",
  outside="infinite W; common knowledge as unbounded protocol; PA-completeness",
  insight=("530 frames = 2+16+512. Reflexive 69, preorder 34, equivalence 8, "
           "serial 353, GL-shape 23. 585 was a leftover string. "
           "Two S5 lookalikes split on contingency."),
  forces=[
   dict(claim="frame counts n=1..3 are 530/69/34/8/353/23",
        check="modal_frame_counts"),
   dict(claim="Löb forced on 23 GL-shaped frames; T fails at empty R",
        check="modal_gl_lob_t")],
  breaks=[
   dict(claim="two isolated loops do not see contingency; S5 blob does",
        check="modal_s5_split")],
  useful_for=["epistemic maps", "deontic D", "provability miniature"]),
]
