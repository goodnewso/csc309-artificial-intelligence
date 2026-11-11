% courses.pl: course prerequisites in Prolog.
% Facts: prereq(Course, Before) means Before must be passed first.
prereq(csc309, csc203).
prereq(csc309, cos201).
prereq(cos201, cos102).
prereq(cos102, cos101).
prereq(csc203, mth101).

passed(amaka, cos101).
passed(amaka, cos102).
passed(amaka, mth101).

% needs(C, X): X must come before C, directly or indirectly (recursion).
needs(C, X) :- prereq(C, X).
needs(C, X) :- prereq(C, Y), needs(Y, X).

% can_take(S, C): S has passed every direct prerequisite of C.
% \+ is negation as failure: "not provable" is taken as false.
can_take(S, C) :- course(C), \+ (prereq(C, X), \+ passed(S, X)).

course(C) :- prereq(C, _).
course(C) :- prereq(_, C).

main :-
    findall(X, needs(csc309, X), L),
    format("Before csc309 you need: ~w~n", [L]),
    setof(C, (can_take(amaka, C), \+ passed(amaka, C)), Next),
    format("Amaka can take next: ~w~n", [Next]),
    ( can_take(amaka, csc309) -> R = yes ; R = no ),
    format("Can Amaka take csc309 now? ~w~n", [R]).
