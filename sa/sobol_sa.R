
setwd('/media/marcelo/OS/dissertacao/')
#
# EHF ----

ehf_s1 = read.csv('s1_ehf.csv')
ehf_s2 = read.csv('s2_ehf.csv')

ehf_s1 = ehf_s1[order(ehf_s1$S1,decreasing = TRUE),]
ehf_s2 = ehf_s2[order(ehf_s2$S2,decreasing = TRUE),]

# TEMP ----

temp_s1 = read.csv('s1_temp.csv')
temp_s2 = read.csv('s2_temp.csv')

temp_s1 = temp_s1[order(temp_s1$S1,decreasing = TRUE),]

# ach ----

ach_s1 = read.csv('s1_ach.csv')
ach_s2 = read.csv('s2_ach.csv')

ach_s1 = ach_s1[order(ach_s1$S1,decreasing = TRUE),]


