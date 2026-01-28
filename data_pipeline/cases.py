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

# 1 from (courses)
s10 = "1 course with a minimum grade of C- from (MATH240, MATH461, MATH341); and 1 course with a minimum grade of C- from (MATH340, MATH241); and 1 course with a minimum grade of C- from (CMSC106, CMSC131); and minimum grade of C- in MATH246."
s11 = "1 course with a minimum grade of C- from (MATH240, MATH461, MATH341); and 1 course with a minimum grade of C- from (MATH340, MATH241); and 1 course with a minimum grade of C- from (CMSC106, CMSC131); and minimum grade of C- in MATH410."
s12 = "ANSC101; and 1 course with a minimum grade of C- from (MATH120, MATH130, MATH136, MATH140)."

# Single Course
s13 = "MATH405."
s14 = "MATH411; or students who have taken courses with comparable content may contact the department."
s15 = "Must have completed AMST201; and 2 courses in AMST."

# Permission + courses
s16 = "ANSC232; or permission of instructor."

print(tokens.tokenize_prereq_string(s6))
print(tree.tokenize(s6))
