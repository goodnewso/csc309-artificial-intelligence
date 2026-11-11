% example_family.pl: facts, a rule and a query.
% Run: swipl -q -g main -t halt example_family.pl
parent(ada, bayo).
parent(bayo, chika).
parent(bayo, dayo).

grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

main :- findall(W, grandparent(ada, W), L),
        format("grandchildren of ada: ~w~n", [L]).
