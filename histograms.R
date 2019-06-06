library(ggplot2)
#
# CONCRETE + EPS ----
samp = read.csv('/media/marcelo/OS/dissertacao/experiment/')
df = rbind(
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster0/means_cluster0.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster1/means_cluster1.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster2/means_cluster2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster3/means_cluster3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster4/means_cluster4.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster5/means_cluster5.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster6/means_cluster6.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster7/means_cluster7.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster8/means_cluster8.csv'),
  read.csv('/media/marcelo/OS/dissertacao/experiment/cluster9/means_cluster9.csv')
)

df_eps = subset(df, substr(df$file,1,1) == 'e')
df_ref = subset(df, substr(df$file,1,1) == 'r')

# df_ref2 = subset(df_ref, df_ref$ehf < .95)
# df_eps = subset(df_eps, df_ref$ehf < .95)
# df_ref = df_ref2

df_dif = data.frame(
  'case' = substr(df_eps$file,5,8),
  'zone' = df_eps$zone,
  'temp' = df_ref$temp - df_eps$temp,
  'ach' = df_ref$ach - df_eps$ach,
  'ehf' = df_ref$ehf - df_eps$ehf
)

ach_mean = mean(df_dif$ach)
ehf_mean = mean(df_dif$ehf)

ggplot(df_dif,aes(df_dif$ehf)) +
  geom_histogram(binwidth = .001)+
  ggtitle('Diferenças no EHF') +
  xlab('EHF Referência - EHF EPS + Concreto') +
  ylab('Número de casos') +
  annotate("text", x = -.02, y = 1000, label = paste("Média =",round(ehf_mean,5))) +
  annotate("text", x = -.02, y = 1000*.95, label = paste("AE95 =",round(quantile(abs(df_dif$ehf),.95),4))) 

ggplot(df_dif,aes(df_dif$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH analítico - ACH tpu') +
  ylab('Número de casos') +
  annotate("text", x = -35, y = 700, label = paste("Média =",round(ach_mean,3),'ach'))


ggplot(df_ref,aes(df_ref$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.8, y = 300, label = paste("Média =",round(mean(df_ref$ehf),5))) +
  annotate("text", x = 0.8, y = 300*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf),.95),4))) 

ggplot(df_ref,aes(df_ref$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('ACH Referência') +
  xlab('ACH') +
  ylab('Número de casos') +
  annotate("text", x = 100, y = 60, label = paste("Média =",round(mean(df_ref$ach),2),'ach'))
# CONCRETE + EPS 2 ----
samp = read.csv('/media/marcelo/OS/dissertacao/sample_diss.csv')

par1_wall_u = 17.5
par1_wall_ct = 220

par2a_wall_u =  3.962
par2a_wall_ct = 138.272

par2b_wall_u = 3.962
par2b_wall_ct = 69.136

par3_wall_u = .773
par3_wall_ct = 29.7875

samp$area = 20+80*samp$area
samp$zone_height = 2.4+.8*samp$zone_height
samp$azimuth = 180*samp$azimuth
samp$ratio = .5 + 1.5*samp$ratio
samp$wwr = .1+.5*samp$wwr
samp$people = .05+.45*samp$people
samp$absorptance = .3 + .6*samp$absorptance

samp = samp[rep(seq_len(nrow(samp)), each=6),]

df = rbind(
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster0/means_cluster0.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster1/means_cluster1.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster2/means_cluster2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster3/means_cluster3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster4/means_cluster4.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster5/means_cluster5.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster6/means_cluster6.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster7/means_cluster7.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster8/means_cluster8.csv'),
  read.csv('/media/marcelo/OS/dissertacao/wall/cluster9/means_cluster9.csv')
)


df_eps_par1 = subset(df, substr(df$file,1,12) == 'epsconc_par1')  # epsconc_par1
df_ref_par1 = subset(df, substr(df$file,1,12) == 'refwall_par1')  # refwall_par1

df_eps_par2a = subset(df, substr(df$file,1,13) == 'epsconc_par2a')  # epsconc_par2a
df_ref_par2a = subset(df, substr(df$file,1,13) == 'refwall_par2a')  # refwall_par2a

df_eps_par2b = subset(df, substr(df$file,1,13) == 'epsconc_par2b')  # epsconc_par2b
df_ref_par2b = subset(df, substr(df$file,1,13) == 'refwall_par2b')  # refwall_par2b

df_eps_par3 = subset(df, substr(df$file,1,12) == 'epsconc_par3')  # epsconc_par3
df_ref_par3 = subset(df, substr(df$file,1,12) == 'refwall_par3')  # refwall_par3

# bind to sample 
df_eps_par1 = cbind(df_eps_par1, samp)
df_ref_par1 = cbind(df_ref_par1, samp)
df_eps_par2a = cbind(df_eps_par2a, samp)
df_ref_par2a = cbind(df_ref_par2a, samp)
df_eps_par2b = cbind(df_eps_par2b, samp)
df_ref_par2b = cbind(df_ref_par2b, samp)
df_eps_par3 = cbind(df_eps_par3, samp)
df_ref_par3 = cbind(df_ref_par3, samp)

df_eps_par1$wall_u = par1_wall_u
df_eps_par1$wall_ct = par1_wall_ct

df_ref_par1$wall_u = par1_wall_u
df_ref_par1$wall_ct = par1_wall_ct

df_eps_par2a$wall_u = par2a_wall_u
df_eps_par2a$wall_ct = par2a_wall_ct

df_ref_par2a$wall_u = par2a_wall_u
df_ref_par2a$wall_ct = par2a_wall_ct

df_eps_par2b$wall_u = par2b_wall_u
df_eps_par2b$wall_ct = par2b_wall_ct

df_ref_par2b$wall_u = par2b_wall_u
df_ref_par2b$wall_ct = par2b_wall_ct

df_eps_par3$wall_u = par3_wall_u
df_eps_par3$wall_ct = par3_wall_ct

df_ref_par3$wall_u = par3_wall_u
df_ref_par3$wall_ct = par3_wall_ct

# df_ref2 = subset(df_ref, df_ref$ehf < .95)
# df_eps = subset(df_eps, df_ref$ehf < .95)
# df_ref = df_ref2

library(corrplot)
cor_matrix_1 = cor(df_ref_par2b[,c("temp","temp_max","ach","ehf","area",
                                         "ratio","zone_height", "azimuth","absorptance", 
                                         "wwr","people")])

corrplot.mixed(cor_matrix_1, lower = "number", upper = "ellipse",
               tl.pos = "lt", number.cex = 0.6, bg = "black",
               tl.col = "black", tl.srt = 90, tl.cex = 0.8)

df_dif_par1 = data.frame(
  'case' = substr(df_eps_par1$file,14,17),
  'zone' = df_eps_par1$zone,
  'temp' = df_ref_par1$temp - df_eps_par1$temp,
  'ach' = df_ref_par1$ach - df_eps_par1$ach,
  'ehf' = df_ref_par1$ehf - df_eps_par1$ehf
)

df_dif_par2a = data.frame(
  'case' = substr(df_eps_par2a$file,14,17),
  'zone' = df_eps_par2a$zone,
  'temp' = df_ref_par2a$temp - df_eps_par2a$temp,
  'ach' = df_ref_par2a$ach - df_eps_par2a$ach,
  'ehf' = df_ref_par2a$ehf - df_eps_par2a$ehf
)

df_dif_par2b = data.frame(
  'case' = substr(df_eps_par2b$file,14,17),
  'zone' = df_eps_par2b$zone,
  'temp' = df_ref_par2b$temp - df_eps_par2b$temp,
  'ach' = df_ref_par2b$ach - df_eps_par2b$ach,
  'ehf' = df_ref_par2b$ehf - df_eps_par2b$ehf
)

df_dif_par3 = data.frame(
  'case' = substr(df_eps_par3$file,14,17),
  'zone' = df_eps_par3$zone,
  'temp' = df_ref_par3$temp - df_eps_par3$temp,
  'ach' = df_ref_par3$ach - df_eps_par3$ach,
  'ehf' = df_ref_par3$ehf - df_eps_par3$ehf
)


tempmax = 40
df_dif_par1 = subset(df_dif_par1, df_ref_par1$temp_max < tempmax)
df_dif_par2a = subset(df_dif_par2a, df_ref_par2a$temp_max < tempmax)
df_dif_par2b = subset(df_dif_par2b, df_ref_par2b$temp_max < tempmax)
df_dif_par3 = subset(df_dif_par3, df_ref_par3$temp_max < tempmax)

ach_mean_par1 = mean(df_dif_par1$ach)
ehf_mean_par1 = mean(df_dif_par1$ehf)

ach_mean_par2a = mean(df_dif_par2a$ach)
ehf_mean_par2a = mean(df_dif_par2a$ehf)
temp_mean_par2a = mean(df_dif_par2a$temp)

ach_mean_par2b = mean(df_dif_par2b$ach)
ehf_mean_par2b = mean(df_dif_par2b$ehf)
temp_mean_par2b = mean(df_dif_par2b$temp)

ach_mean_par3 = mean(df_dif_par3$ach)
ehf_mean_par3 = mean(df_dif_par3$ehf)

df_dif = rbind(df_dif_par1, df_dif_par2b,df_dif_par3)
ach_mean = mean(df_dif$ach)
ehf_mean = mean(df_dif$ehf)

ggplot(df_dif,aes(df_dif$ehf)) +
  geom_histogram(binwidth = .001)+
  ggtitle('Diferenças no EHF') +
  xlab('EHF Referência - EHF EPS + Concreto') +
  ylab('Número de casos') +
  annotate("text", x = -.02, y = 1000, label = paste("Média =",round(ehf_mean,5))) +
  annotate("text", x = -.02, y = 1000*.95, label = paste("AE95 =",round(quantile(abs(df_dif$ehf),.95),4))) 

ggplot(df_dif,aes(df_dif$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH analítico - ACH tpu') +
  ylab('Número de casos') +
  annotate("text", x = -35, y = 700, label = paste("Média =",round(ach_mean,3),'ach'))

df_ref = subset(df, substr(df$file,1,1) == 'r' &  df$temp_max < tempmax)  # refwall_par1

ggplot(df_ref,aes(df_ref$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.8, y = 300, label = paste("Média =",round(mean(df_ref$ehf),5))) +
  annotate("text", x = 0.8, y = 300*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf),.95),4))) 

ggplot(df_ref,aes(df_ref$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('ACH Referência') +
  xlab('ACH') +
  ylab('Número de casos') +
  annotate("text", x = 100, y = 60, label = paste("Média =",round(mean(df_ref$ach),2),'ach'))

# OUTDOORS x ADIABATIC ----

df = rbind(
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster0/means_cluster0.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster1/means_cluster1.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster2/means_cluster2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster3/means_cluster3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster4/means_cluster4.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster5/means_cluster5.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster6/means_cluster6.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster7/means_cluster7.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster8/means_cluster8.csv'),
  read.csv('/media/marcelo/OS/dissertacao/noafn/cluster9/means_cluster9.csv')
)

df_out = subset(df, substr(df$file,1,1) == 'o')
df_adi = subset(df, substr(df$file,1,1) == 'a')
df_ref = subset(df, substr(df$file,1,1) == 'w')

df_out <- df_out[order(df_out$file),]
df_adi <- df_adi[order(df_adi$file),]

df_dif_out = data.frame(
  'case' = substr(df_out$file,10,12),
  'zone' = df_out$zone,
  'temp' = df_ref$temp - df_out$temp,
  'ehf' = df_ref$ehf - df_out$ehf
)
df_dif_adi = data.frame(
  'case' = substr(df_adi$file,11,13),
  'zone' = df_adi$zone,
  'temp' = df_ref$temp - df_adi$temp,
  'ehf' = df_ref$ehf - df_adi$ehf
)

ehf_mean_out = mean(df_dif_out$ehf)

ehf_mean_adi = mean(df_dif_adi$ehf)

dif_out_adi = df_dif_out$ehf - df_dif_adi$ehf
max(dif_out_adi)
min(dif_out_adi)  # erros sempre maiores no outdoors!

ggplot(df_dif_out,aes(df_dif_out$ehf)) +
  geom_histogram(binwidth = .001)+
  ggtitle('Diferenças no EHF Outdoors') +
  xlab('EHF Referência - EHF EPS + Concreto') +
  ylab('Número de casos') +
  annotate("text", x = 0.25, y = 95, label = paste("Média =",round(ehf_mean_out,5))) +
  annotate("text", x = 0.25, y = 95*.95, label = paste("AE95 =",round(quantile(abs(df_dif_out$ehf),.95),4))) 

ggplot(df_dif_adi,aes(df_dif_adi$ehf)) +
  geom_histogram(binwidth = .001)+
  ggtitle('Diferenças no EHF Adiabático') +
  xlab('EHF Whole - EHF Singlezone') +
  ylab('Número de casos') +
  annotate("text", x = -.07, y = 120, label = paste("Média =",round(ehf_mean_adi,5))) +
  annotate("text", x = -.07, y = 120*.95, label = paste("AE95 =",round(quantile(abs(df_dif_adi$ehf),.95),4))) 


ggplot(df_ref,aes(df_ref$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.6, y = 120, label = paste("Média =",round(mean(df_ref$ehf),5))) +
  annotate("text", x = 0.6, y = 120*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf),.95),4))) 

# Cp Eq ----

df = rbind(
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster0/means_cluster0.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster1/means_cluster1.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster2/means_cluster2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster3/means_cluster3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster4/means_cluster4.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster5/means_cluster5.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster6/means_cluster6.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster7/means_cluster7.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster8/means_cluster8.csv'),
  read.csv('/media/marcelo/OS/dissertacao/validatecp/cluster9/means_cluster9.csv')
)

# df_noeq = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster0/sz_means_cluster0.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster1/sz_means_cluster1.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster2/sz_means_cluster2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster3/sz_means_cluster3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster4/sz_means_cluster4.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster5/sz_means_cluster5.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster6/sz_means_cluster6.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster7/sz_means_cluster7.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster8/sz_means_cluster8.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster9/sz_means_cluster9.csv')
# )

# samp = read.csv('/media/marcelo/OS/dissertacao/sample_cpeq.csv')

for(i in 0:3){
df_cpeq = subset(df, substr(df$file,1,2) == 'cp')
df_noeq = subset(df, substr(df$file,1,2) == 'no')
df_ref = subset(df, substr(df$file,1,1) == 'w')

df_noeq <- df_noeq[order(df_noeq$file),]
df_cpeq <- df_cpeq[order(df_cpeq$file),]
df_ref <- df_ref[order(df_ref$file),]

ehfmin= .6+(i*.1)
ehfmax = .7+(i*.1)
df_ref2 = subset(df_ref, df_ref$ehf > ehfmin & df_ref$ehf < ehfmax)
df_cpeq = subset(df_cpeq, df_ref$ehf > ehfmin & df_ref$ehf < ehfmax)
df_noeq = subset(df_noeq, df_ref$ehf > ehfmin & df_ref$ehf < ehfmax)

# tempmax = 40
# df_ref2 = subset(df_ref, df_ref$temp_max < tempmax) #.95)
# df_cpeq = subset(df_cpeq, df_ref$temp_max < tempmax) #.95)
# df_noeq = subset(df_noeq, df_ref$temp_max < tempmax) #.95)

df_ref = df_ref2

df_dif_cpeq = data.frame(
  'case' = substr(df_cpeq$file,6,9),
  'zone' = df_cpeq$zone,
  'ach' = df_ref$ach - df_cpeq$ach,
  'temp' = df_ref$temp - df_cpeq$temp,
  'ehf' = df_ref$ehf - df_cpeq$ehf
)

df_dif_noeq = data.frame(
  'case' = substr(df_noeq$file,6,9),
  'zone' = df_noeq$zone,
  'ach' = df_ref$ach - df_noeq$ach,
  'temp' = df_ref$temp - df_noeq$temp,
  'ehf' = df_ref$ehf - df_noeq$ehf
)

ehf_mean_cpeq = mean(df_dif_cpeq$ehf)
max(df_dif_cpeq$ehf)
min(df_dif_cpeq$ehf)

temp_mean_cpeq = mean(df_dif_cpeq$temp)
max(df_dif_cpeq$temp)

ach_mean_cpeq = mean(df_dif_cpeq$ach)
max(df_dif_cpeq$ach)
min(df_dif_cpeq$ach)

ehf_mean_noeq = mean(df_dif_noeq$ehf)
max(df_dif_noeq$ehf)

temp_mean_noeq = mean(df_dif_noeq$temp)
max(df_dif_noeq$temp)

ach_mean_noeq = mean(df_dif_noeq$ach)
max(df_dif_noeq$ach)
min(df_dif_noeq$ach)

print(ehf_mean_cpeq)
print(ehf_mean_noeq)
}

ggplot(df_dif_cpeq,aes(df_dif_cpeq$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('Diferenças no EHF Cp equivalente') +
  xlab('EHF Referência - EHF Cp_eq') +
  ylab('Número de casos') #+
  # xlim(c(-.1,.1)) +
  # xlim(c(-.3,.22)) +
  ylim(c(0,8)) +
  annotate("text", x = -0.1, y = 7, label = paste("Média =",round(ehf_mean_cpeq,5))) +
  annotate("text", x = -0.1, y = 7*.93, label = paste("AE95 =",round(quantile(abs(df_dif_cpeq$ehf),.95),4))) 
#   annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_noeq,5))) +
#   annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_noeq$ehf),.95),4))) 

ggplot(df_dif_cpeq,aes(df_dif_cpeq$temp)) +
  geom_histogram(binwidth = .5)+
  ggtitle('Diferenças no TEMP Cp equivalente') +
  xlab('TEMP Referência - TEMP Cp_eq') +
  ylab('Número de casos') #+
  xlim(c(-.1,.1)) +
  annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_cpeq,5))) +
  annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_cpeq$ehf),.95),4))) 

ggplot(df_dif_cpeq,aes(df_dif_cpeq$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos')# +
  # ylim(c(0,1100)) +
  annotate("text", x = 20, y = 2000, label = paste("Média =",round(ach_mean_cpeq,3),'ach'))


ggplot(df_dif_noeq,aes(df_dif_noeq$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('Diferenças no EHF no equivalente') +
  xlab('EHF Referência - EHF no_eq') +
  ylab('Número de casos') #+
  # xlim(c(-.1,.1)) +
  xlim(c(-.3,.2)) +
  ylim(c(0,8)) +
  annotate("text", x = -0.1, y = 7, label = paste("Média =",round(ehf_mean_noeq,5))) +
  annotate("text", x = -0.1, y = 7*.93, label = paste("AE95 =",round(quantile(abs(df_dif_noeq$ehf),.95),4))) 
#   annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_noeq,5))) +
#   annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_noeq$ehf),.95),4))) 

ggplot(df_dif_noeq,aes(df_dif_noeq$temp)) +
  geom_histogram(binwidth = .5)+
  ggtitle('Diferenças no TEMP no equivalente') +
  xlab('EHF Referência - EHF no_eq') +
  ylab('Número de casos') #+
  xlim(c(-.1,.1)) +
  annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_noeq,5))) +
  annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_noeq$ehf),.95),4))) 
  
ggplot(df_dif_noeq,aes(df_dif_noeq$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH no_eq') +
  ylab('Número de casos') #+
  # ylim(c(0,1100)) +
  annotate("text", x = 20, y = 2000, label = paste("Média =",round(ach_mean_noeq,3),'ach'))


ggplot(df_ref,aes(df_ref$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos')# +
  annotate("text", x = 0.8, y = 3500, label = paste("Média =",round(mean(df_ref$ehf),5))) +
  annotate("text", x = 0.8, y = 3500*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf),.95),4))) 
quantile(abs(df_ref$ehf),.05)

ggplot(df_ref,aes(df_ref$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('ACH Referência') +
  xlab('ACH') +
  ylab('Número de casos') #+
  annotate("text", x = 20, y = 750, label = paste("Média =",round(mean(df_ref$ach),2),'ach'))

df_single_0413_3 = read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster4/single_0413_3out.csv')
max(df_single_0413_3$OFFICE.Zone.Operative.Temperature..C..Hourly.)
mean(df_single_0413_3$OFFICE.Zone.Operative.Temperature..C..Hourly.[df_single_0413_3$SCH_OCUPACAO.Schedule.Value....Hourly. > 0])


#
# CRACK faltou crack nos modelos de duas janelas!!!!! ----

df = rbind(
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster0/means_cluster0.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster1/means_cluster1.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster2/means_cluster2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster3/means_cluster3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster4/means_cluster4.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster5/means_cluster5.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster6/means_cluster6.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster7/means_cluster7.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster8/means_cluster8.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster9/means_cluster9.csv')
)

df_2 = rbind(
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster0/means_cluster0_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster1/means_cluster1_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster2/means_cluster2_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster3/means_cluster3_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster4/means_cluster4_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster5/means_cluster5_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster6/means_cluster6_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster7/means_cluster7_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster8/means_cluster8_2.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster9/means_cluster9_2.csv')
)

df_3 = rbind(
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster0/means_cluster0_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster1/means_cluster1_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster2/means_cluster2_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster3/means_cluster3_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster4/means_cluster4_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster5/means_cluster5_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster6/means_cluster6_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster7/means_cluster7_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster8/means_cluster8_3.csv'),
  read.csv('/media/marcelo/OS/dissertacao/crack/cluster9/means_cluster9_3.csv')
)

df_ref = subset(df, substr(df$file,1,1) == 'w')  # & df$ehf < .9)
df_001 = subset(df, substr(df$file,1,3) == '001')  # & df_ref$ehf < .9)
df_010 = subset(df, substr(df$file,1,3) == '010')  # & df_ref$ehf < .9)
df_100 = subset(df, substr(df$file,1,3) == '100')  # & df_ref$ehf < .9)

df_020 = subset(df_2, substr(df_2$file,1,3) == '020')  # & df_ref$ehf < .9)
df_050 = subset(df_2, substr(df_2$file,1,3) == '050')  # & df_ref$ehf < .9)

df_015 = subset(df_3, substr(df_3$file,1,3) == '015')  # & df_ref$ehf < .9)

# threshold = .8
# df_001 = subset(df_001, df_ref$ehf < threshold)
# df_010 = subset(df_010, df_ref$ehf < threshold)
# df_100 = subset(df_100, df_ref$ehf < threshold)
# df_020 = subset(df_020, df_ref$ehf < threshold)
# df_050 = subset(df_050, df_ref$ehf < threshold)
# df_015 = subset(df_015, df_ref$ehf < threshold)
# 
# df_ref = subset(df_ref, df_ref$ehf < threshold)

df_015 <- df_015[order(df_015$file),]

df_020 <- df_020[order(df_020$file),]
df_050 <- df_050[order(df_050$file),]

df_001 <- df_001[order(df_001$file),]
df_010 <- df_010[order(df_010$file),]
df_100 <- df_100[order(df_100$file),]
df_ref <- df_ref[order(df_ref$file),]

df_dif_001 = data.frame(
  'case' = substr(df_001$file,10,12),
  'zone' = df_001$zone,
  'ach' = df_ref$ach - df_001$ach,
  'temp' = df_ref$temp - df_001$temp,
  'ehf' = df_ref$ehf - df_001$ehf
)

df_dif_010 = data.frame(
  'case' = substr(df_010$file,10,12),
  'zone' = df_010$zone,
  'ach' = df_ref$ach - df_010$ach,
  'temp' = df_ref$temp - df_010$temp,
  'ehf' = df_ref$ehf - df_010$ehf
)

df_dif_015 = data.frame(
  'case' = substr(df_015$file,10,12),
  'zone' = df_015$zone,
  'ach' = df_ref$ach - df_015$ach,
  'temp' = df_ref$temp - df_015$temp,
  'ehf' = df_ref$ehf - df_015$ehf
)

df_dif_020 = data.frame(
  'case' = substr(df_020$file,10,12),
  'zone' = df_020$zone,
  'ach' = df_ref$ach - df_020$ach,
  'temp' = df_ref$temp - df_020$temp,
  'ehf' = df_ref$ehf - df_020$ehf
)

df_dif_050 = data.frame(
  'case' = substr(df_050$file,10,12),
  'zone' = df_050$zone,
  'ach' = df_ref$ach - df_050$ach,
  'temp' = df_ref$temp - df_050$temp,
  'ehf' = df_ref$ehf - df_050$ehf
)

df_dif_100 = data.frame(
  'case' = substr(df_100$file,10,12),
  'zone' = df_100$zone,
  'ach' = df_ref$ach - df_100$ach,
  'temp' = df_ref$temp - df_100$temp,
  'ehf' = df_ref$ehf - df_100$ehf
)

ehf_mean_001 = mean(df_dif_001$ehf)
max(df_dif_001$ehf)

ach_mean_001 = mean(df_dif_001$ach)
max(df_dif_001$ach)
min(df_dif_001$ach)

ehf_mean_010 = mean(df_dif_010$ehf)
max(df_dif_010$ehf)

ach_mean_010 = mean(df_dif_010$ach)
max(df_dif_010$ach)
min(df_dif_010$ach)

ehf_mean_015 = mean(df_dif_015$ehf)
max(df_dif_015$ehf)

ach_mean_015 = mean(df_dif_015$ach)
max(df_dif_015$ach)
min(df_dif_015$ach)

ehf_mean_100 = mean(df_dif_100$ehf)
max(df_dif_100$ehf)

ach_mean_100 = mean(df_dif_100$ach)
max(df_dif_100$ach)
min(df_dif_100$ach)

ehf_mean_020 = mean(df_dif_020$ehf)
max(df_dif_020$ehf)

ach_mean_020 = mean(df_dif_020$ach)
max(df_dif_020$ach)
min(df_dif_020$ach)

ehf_mean_050 = mean(df_dif_050$ehf)
max(df_dif_050$ehf)

ach_mean_050 = mean(df_dif_050$ach)
max(df_dif_050$ach)
min(df_dif_050$ach)

# ggplot(df_dif_001,aes(df_dif_001$ehf)) +
#   geom_histogram(binwidth = .005)+
#   ggtitle('Diferenças no EHF Cp equivalente') +
#   xlab('EHF Referência - EHF Cp_eq') +
#   ylab('Número de casos') #+
#   xlim(c(-.1,.1)) +
#   annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_001,5))) +
#   annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_001$ehf),.95),4))) 

ggplot(df_dif_001,aes(df_dif_001$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(ach_mean_001,3),'ach'))

# ggplot(df_dif_010,aes(df_dif_010$ehf)) +
#   geom_histogram(binwidth = .005)+
#   ggtitle('Diferenças no EHF Cp equivalente') +
#   xlab('EHF Referência - EHF Cp_eq') +
#   ylab('Número de casos') #+
#   xlim(c(-.1,.1)) +
#   annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_010,5))) +
#   annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_010$ehf),.95),4))) 

ggplot(df_dif_010,aes(df_dif_010$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(ach_mean_010,3),'ach'))

ggplot(df_dif_015,aes(df_dif_015$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(ach_mean_015,3),'ach'))

# ggplot(df_dif_100,aes(df_dif_100$ehf)) +
#   geom_histogram(binwidth = .005)+
#   ggtitle('Diferenças no EHF Cp equivalente') +
#   xlab('EHF Referência - EHF Cp_eq') +
#   ylab('Número de casos') +
#   xlim(c(-.1,.1)) +
#   annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_100,5))) +
#   annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_100$ehf),.95),4))) 

ggplot(df_dif_100,aes(df_dif_100$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(ach_mean_100,3),'ach'))

# ggplot(df_dif_020,aes(df_dif_020$ehf)) +
#   geom_histogram(binwidth = .005)+
#   ggtitle('Diferenças no EHF Cp equivalente') +
#   xlab('EHF Referência - EHF Cp_eq') +
#   ylab('Número de casos') +
#   xlim(c(-.1,.1)) +
#   annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_020,5))) +
#   annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_020$ehf),.95),4))) 

ggplot(df_dif_020,aes(df_dif_020$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(ach_mean_020,3),'ach'))

# ggplot(df_dif_050,aes(df_dif_050$ehf)) +
#   geom_histogram(binwidth = .005)+
#   ggtitle('Diferenças no EHF Cp equivalente') +
#   xlab('EHF Referência - EHF Cp_eq') +
#   ylab('Número de casos') +
#   xlim(c(-.1,.1)) +
#   annotate("text", x = -0.08, y = 3000, label = paste("Média =",round(ehf_mean_050,5))) +
#   annotate("text", x = -0.08, y = 3000*.93, label = paste("AE95 =",round(quantile(abs(df_dif_050$ehf),.95),4))) 

ggplot(df_dif_050,aes(df_dif_050$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(ach_mean_050,3),'ach'))


ggplot(df_ref,aes(df_ref$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos')# +
  annotate("text", x = 0.8, y = 3500, label = paste("Média =",round(mean(df_ref$ehf),5))) +
  annotate("text", x = 0.8, y = 3500*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf),.95),4)))

ggplot(df_ref,aes(df_ref$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('ACH Referência') +
  xlab('ACH') +
  ylab('Número de casos') +
  annotate("text", x = 20, y = 750, label = paste("Média =",round(mean(df_ref$ach),2),'ach'))

# samps ----

samp = read.csv('/media/marcelo/OS/dissertacao/sample_cpeq.csv')

case_413 = read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster4/single_0412_3out.csv')
whole_413 = read.csv('/media/marcelo/OS/dissertacao/cpeq/cluster4/whole_0412out.csv')
