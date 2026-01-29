import tree
import tokens

# OR separated courses
s1 = "AASP101 or AASP202."
s2 = "AASP100 or HIST157."
s3 = "AASP202 or AASP100."

# Complex AND/OR combinations
s4 = "AASP101; and (ECON201 or ECON200)."
s5 = "CMSC660 or AMSC660; and (CMSC661 or AMSC661)."
s6 = "BSCI105; or (BSCI170 and BSCI171); or permission of AGNR-Animal & Avian Sciences department; or students who have taken courses with comparable content may contact the department."

# AND separated courses
s7 = "AASP386 and AASP297."
s8 = "CMSC466 or AMSC466; and MATH410."
s9 = "AMST201 and AMST340; and 1 course in AMST."

# 1 from (courses) - Grade requirements
s10 = "1 course with a minimum grade of C- from (MATH240, MATH461, MATH341); and 1 course with a minimum grade of C- from (MATH340, MATH241); and 1 course with a minimum grade of C- from (CMSC106, CMSC131); and minimum grade of C- in MATH246."
s11 = "1 course with a minimum grade of C- from (MATH240, MATH461, MATH341); and 1 course with a minimum grade of C- from (MATH340, MATH241); and 1 course with a minimum grade of C- from (CMSC106, CMSC131); and minimum grade of C- in MATH410."
s12 = "ANSC101; and 1 course with a minimum grade of C- from (MATH120, MATH130, MATH136, MATH140)."

# Single Course
s13 = "MATH405."
s14 = "MATH411; or students who have taken courses with comparable content may contact the department."
s15 = "Must have completed AMST201; and 2 courses in AMST."

# Permission + courses
s16 = "ANSC232; or permission of instructor."

# Additional formats from test.py - Complex grade requirements with permission
s17 = "1 course with a minimum grade of C- from (CMSC414, CMSC417, CMSC420, CMSC430, CMSC433, CMSC435, ENEE440, ENEE457); and permission of ENGR-Electrical & Computer Engineering department; and (ENEE350, CMSC330, and CMSC351)."
s18 = "Minimum grade of C- in CMSC132; and 1 course with a minimum grade of C- from (MATH141, MATH142); and permission of department."
s19 = "1 course with a minimum grade of C- from (CMSC412, CMSC417, CMSC420); and 1 course with a minimum grade of C- from (ENEE440, ENEE447); and permission of CMNS-Computer Science department."
s20 = "Minimum grade of C- in (CMSC132 OR CMSC216); and 1 course with a minimum grade of C- from (STAT100, STAT400); and (MATH140 OR MATH141)."
s21 = "Minimum grade of C- in CMSC132; and minimum grade of C- in CMSC216; and minimum grade of C- in CMSC250."

# Prerequisite prefix cases
s22 = "Prerequisite: (CMSC216 OR CMSC226); and (MATH141 OR MATH140); and PHYS161."
s23 = "Prerequisite: ((CMSC414 OR CMSC417) OR CMSC420); and (ENEE350, CMSC330, CMSC351)."
s24 = "Prerequisite: (CMSC412, CMSC417, CMSC420); or permission of instructor."
s25 = "Prerequisite: (CMSC216 OR CMSC226); and ((MATH141 AND PHYS161) OR MATH140)."

# Complex nested parentheses
s26 = "1 course with a minimum grade of C- from (CMSC414, CMSC417, CMSC420, CMSC430); and 1 course with a minimum grade of C- from (MATH141, MATH142, STAT100); and PHYS161."
s27 = "Corequisite: (CMSC216 OR CMSC226); and (MATH141 OR MATH140)."

# Simple course chain prerequisites
s28 = "ARAB105; and ARAB204; and ARAB315."
s29 = "MATH107; and MATH110; and MATH115."
s30 = "ANTH260."

lst = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30]
i = 0
#print(tree.tokenize(s16))
tree.print_node(tree.treeify(s15))
#for s in lst:
#    print(f"Run #{i}")
#    tree.print_node(tree.treeify(s))
#    i += 1