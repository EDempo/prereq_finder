import tree
import json

#################
#   TESTING    #
# # # ## ## # # 
def test_prereqs(s, expected, i):
    print(f"||| RUN #{i} |||")
    node = tree.treeify(s)
    print(f"\n\n\nTEST.PY\n\n\n returned node was: {tree.print_node(node)}")

    print("This is the expected node:\n")
    tree.print_node(expected)
    print("\nThis is the result node:\n")
    tree.print_node(node)
    if(node == expected):
        print(f"On run {i}, same same")
    else:
        print(f"On run {i}, diff diff")



def test():
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
    
    e = tree.courseNode(
                "AND", [tree.courseNode("OR",
                                        ["CMSC414", "CMSC417", "CMSC420", "CMSC430", "CMSC433", "CMSC435", "ENEE440", "ENEE457"]),
                        tree.courseNode("AND",
                                        ["ENEE350", "CMSC330", "CMSC351"])
                        ]
                )
    
    e1 = tree.courseNode(
        "AND", [
            tree.courseNode(
                "OR",
                ["CMSC414", "CMSC417", "CMSC420", "CMSC430",
                 "CMSC433", "CMSC435", "ENEE440", "ENEE457"]
            ),
            tree.courseNode(
                "AND",
                ["ENEE350", "CMSC330", "CMSC351"]
            )
        ]
    )
    
    e2 = tree.courseNode(
        "AND", [
            "CMSC132",
            tree.courseNode(
                "OR",
                ["MATH141", "MATH142"]
            )
        ]
    )
    
    
    e3 = tree.courseNode(
        "AND", [
            tree.courseNode(
                "OR",
                ["CMSC216", "CMSC226"]
            ),
            tree.courseNode(
                "OR",
                ["MATH141", "MATH140"]
            ),
            "PHYS161"
        ]
    )
    
    
    e4 = tree.courseNode(
        "AND", [
            tree.courseNode(
                "OR",
                ["CMSC412", "CMSC417", "CMSC420"]
            ),
            tree.courseNode(
                "OR",
                ["ENEE440", "ENEE447"]
            )
        ]
    )
    
    
    e5 = tree.courseNode(
        "AND", [
            tree.courseNode(
                "OR",
                ["CMSC414", "CMSC417", "CMSC420"]
            ),
            tree.courseNode(
                "OR",
                ["ENEE350", "CMSC330", "CMSC351"]
            )
        ]
    )
    
    
    e6 = tree.courseNode(
        "AND", [
            tree.courseNode(
                "OR",
                ["CMSC132", "CMSC216"]
            ),
            tree.courseNode(
                "OR",
                ["STAT100", "STAT400"]
            ),
            tree.courseNode(
                "OR",
                ["MATH140", "MATH141"]
            )
        ]
    )
    
    e7 = tree.courseNode(
        "OR",
        ["CMSC412", "CMSC417", "CMSC420"]
    )
    
    e8 = tree.courseNode(
        "AND", [
            tree.courseNode(
                "OR",
                ["CMSC414", "CMSC417", "CMSC420", "CMSC430"]
            ),
            tree.courseNode(
                "OR",
                ["MATH141", "MATH142", "STAT100"]
            ),
            "PHYS161"
        ]
    )
    
    
    e9 = tree.courseNode(
        "AND", [
            tree.courseNode(
                "OR",
                ["CMSC216", "CMSC226"]
            ),
            tree.courseNode(
                "OR", [
                    tree.courseNode(
                        "AND",
                        ["MATH141", "PHYS161"]
                    ),
                    "MATH140"
                ]
            )
        ]
    )
    
    
    e10 = tree.courseNode(
        "AND",
        ["CMSC132", "CMSC216", "CMSC250"]
    )
    
    s_lst = [ s, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    e_lst = [ e, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]
    
    for i in range(11):
        test_prereqs(s_lst[i], e_lst[i], i)

test()
