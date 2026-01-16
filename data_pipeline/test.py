import tree
import json

#################
#   TESTING    #
# # # ## ## # # 
def test_prereqs():
    s = ("1 course with a minimum grade of C- from (CMSC414, CMSC417, CMSC420, CMSC430, CMSC433, CMSC435, ENEE440, ENEE457);" 
                "and permission of ENGR-Electrical & Computer Engineering department;"
                 "and (ENEE350, CMSC330, and CMSC351)."
                )

    s1 = (
        "1 course with a minimum grade of C- from "
        "(CMSC414, CMSC417, CMSC420, CMSC430, CMSC433, CMSC435, ENEE440, ENEE457); "
        "and (ENEE350, CMSC330, and CMSC351)."
    )
    
    s2 = (
        "Minimum grade of C- in CMSC132; "
        "and 1 course with a minimum grade of C- from "
        "(MATH141, MATH142); "
        "and permission of department."
    )
    
    s3 = (
        "Prerequisite: "
        "(CMSC216 OR CMSC226); "
        "and (MATH141 OR MATH140); "
        "and PHYS161."
    )
    
    s4 = (
        "1 course with a minimum grade of C- from "
        "(CMSC412, CMSC417, CMSC420); "
        "and 1 course with a minimum grade of C- from "
        "(ENEE440, ENEE447); "
        "and permission of CMNS-Computer Science department."
    )
    
    s5 = (
        "Prerequisite: "
        "((CMSC414 OR CMSC417) OR CMSC420); "
        "and (ENEE350, CMSC330, CMSC351)."
    )
    
    s6 = (
        "Minimum grade of C- in "
        "(CMSC132 OR CMSC216); "
        "and 1 course with a minimum grade of C- from "
        "(STAT100, STAT400); "
        "and (MATH140 OR MATH141)."
    )
    
    s7 = (
        "Prerequisite: "
        "(CMSC412, CMSC417, CMSC420); "
        "or permission of instructor."
    )
    
    s8 = (
        "1 course with a minimum grade of C- from "
        "(CMSC414, CMSC417, CMSC420, CMSC430); "
        "and 1 course with a minimum grade of C- from "
        "(MATH141, MATH142, STAT100); "
        "and PHYS161."
    )
    
    s9 = (
        "Prerequisite: "
        "(CMSC216 OR CMSC226); "
        "and ((MATH141 AND PHYS161) OR MATH140)."
    )
    
    s10 = (
        "Minimum grade of C- in CMSC132; "
        "and minimum grade of C- in CMSC216; "
        "and minimum grade of C- in CMSC250."
    )
    node = tree.treeify(s)
    print(f"\n\n\nTEST.PY\n\n\n returned node was: {tree.print_node(node)}")
    expected  = tree.courseNode(
            "AND", [tree.courseNode("OR",
                                    ["CMSC414", "CMSC417", "CMSC420", "CMSC430", "CMSC433", "CMSC435", "ENEE440", "ENEE457"]),
                    tree.courseNode("AND",
                                    ["ENEE350", "CMSC330", "CMSC351"])
                    ]
            )

    print("This is the expected node:\n")
    tree.print_node(expected)
    print("\nThis is the result node:\n")
    tree.print_node(node)
    assert node == expected, "full"
    print("hi")
    tree.print_node(node)


#test_factor_course()
#print("1")
#test_factor_parens()
#print("2")
#test_term_or_chain()
#print("3")
#test_expression_and_or()
#print("4")
test_full_prereq()
print("all good!")
