library(ggplot2)
library(corrplot)
#
save_img = function(name,fact=1,square=FALSE){
  if(square){
  width = 100* fact
  height = 100 * fact
  }else{width = 145* fact
  height = 90 * fact
  }
  file_name = paste('~/dissertacao/latex/img/',name,'.png', sep='')
  ggsave(file_name, width = width, height = height,units = 'mm')
}

erro.medio = function(x,y){
  z = x-y
  return(mean(z))
}
erro.absoluto = function(x,y){
  z = abs(x-y)
  return(mean(z))
}
erro.ae95 = function(x,y,p=.95){
  z = abs(x-y)
  return(quantile(z,p))
}
rmse = function(x,y){
  z = (mean((x-y)**2))**(1/2)
  return(z)
}

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
# samp = read.csv('/media/marcelo/OS/dissertacao/sample_diss.csv')
samp = read.csv('/media/marcelo/OS/dissertacao/sample_eq_wall.csv')

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

# df = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster0/means_cluster0.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster1/means_cluster1.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster2/means_cluster2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster3/means_cluster3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster4/means_cluster4.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster5/means_cluster5.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster6/means_cluster6.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster7/means_cluster7.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster8/means_cluster8.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/wall/cluster9/means_cluster9.csv')
# )
# 
# df = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster0/means_parede_eq_cluster0.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster1/means_parede_eq_cluster1.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster2/means_parede_eq_cluster2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster3/means_parede_eq_cluster3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster4/means_parede_eq_cluster4.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster5/means_parede_eq_cluster5.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster6/means_parede_eq_cluster6.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster7/means_parede_eq_cluster7.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster8/means_parede_eq_cluster8.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/parede_eq/cluster9/means_parede_eq_cluster9.csv')
# )

df = read.csv('/media/marcelo/OS/dissertacao/parede_eq/means_parede_eq.csv')

df_eps_par1 = subset(df, grepl(pattern = 'eq_par1',df$file))  # epsconc_par1
df_ref_par1 = subset(df, grepl(pattern = 'ref_par1',df$file))   # refwall_par1

df_eps_par2a = subset(df, grepl(pattern = 'eq_par2a',df$file))   # epsconc_par2a
df_ref_par2a = subset(df, grepl(pattern = 'ref_par2b',df$file))   # refwall_par2a

df_eps_par2b = subset(df, grepl(pattern = 'eq_par2b',df$file))   # epsconc_par2b
df_ref_par2b = subset(df, grepl(pattern = 'ref_par2b',df$file))   # refwall_par2b

df_eps_par3 = subset(df, grepl(pattern = 'eq_par3',df$file))   # epsconc_par3
df_ref_par3 = subset(df, grepl(pattern = 'ref_par3',df$file))   # refwall_par3

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
temp_mean_par1 = mean(df_dif_par1$temp)

ach_mean_par2a = mean(df_dif_par2a$ach)
ehf_mean_par2a = mean(df_dif_par2a$ehf)
temp_mean_par2a = mean(df_dif_par2a$temp)

ach_mean_par2b = mean(df_dif_par2b$ach)
ehf_mean_par2b = mean(df_dif_par2b$ehf)
temp_mean_par2b = mean(df_dif_par2b$temp)

ach_mean_par3 = mean(df_dif_par3$ach)
ehf_mean_par3 = mean(df_dif_par3$ehf)
temp_mean_par3 = mean(df_dif_par3$temp)

df_dif = rbind(df_dif_par1, df_dif_par2b,df_dif_par3)
ach_mean = mean(df_dif$ach)
ehf_mean = mean(df_dif$ehf)

# EHFSCATTERPLOT
ggplot(df_ref_par1,aes(df_ref_par1$ehf, df_eps_par1$ehf)) +
  geom_point(alpha=.1) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1))

ggplot(df_ref_par2a,aes(df_ref_par2a$ehf, df_eps_par2a$ehf)) +
  geom_point(alpha=.25) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1)) +
  # ggtitle('Comparação EHF Alvenaria inteira') +
  xlab('Parede Referência - EHF (-)') +
  ylab('Parede Equivalente - valor total da CT\nEHF (-)') +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(erro.medio(df_ref_par2a$ehf, df_eps_par2a$ehf),4))) +
  annotate("text", x = .2, y = .8, label = paste("AE95 = ",round(erro.ae95(df_ref_par2a$ehf, df_eps_par2a$ehf),4),0,sep=''))
save_img('paredeeq_EHF_par2a_scatter')
mean(df_ref_par2a$ehf-df_eps_par2a$ehf)
mean(abs(df_ref_par2a$ehf-df_eps_par2a$ehf))
quantile((abs(df_ref_par2a$ehf-df_eps_par2a$ehf)),.95)

ggplot(df_ref_par2b,aes(df_ref_par2b$ehf, df_eps_par2b$ehf)) +
  geom_point(alpha=.25) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1)) +
  # ggtitle('Comparação EHF Alvenaria Metade') +
  xlab('Parede Referência - EHF (-)') +
  ylab('Parede Equivalente - metade do valor da CT\nEHF (-)') +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(erro.medio(df_ref_par2b$ehf, df_eps_par2b$ehf),4))) +
  annotate("text", x = .2, y = .8, label = paste("AE95 =",round(erro.ae95(df_ref_par2b$ehf, df_eps_par2b$ehf),4)))
save_img('paredeeq_EHF_par2b_scatter')
mean(df_ref_par2b$ehf-df_eps_par2b$ehf)
mean(abs(df_ref_par2b$ehf-df_eps_par2b$ehf))
quantile((abs(df_ref_par2b$ehf-df_eps_par2b$ehf)),.95)

ggplot(df_ref_par3,aes(df_ref_par3$ehf, df_eps_par3$ehf)) +
  geom_point(alpha=.25) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1)) +
  # ggtitle('Comparação EHF Gesso + Isolamento') +
  xlab('Parede Referência - EHF (-)') +
  ylab('Parede Equivalente - EHF (-)') +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(erro.medio(df_ref_par3$ehf, df_eps_par3$ehf),4))) +
  annotate("text", x = .2, y = .8, label = paste("AE95 =",round(erro.ae95(df_ref_par3$ehf, df_eps_par3$ehf),4)))
save_img('paredeeq_EHF_par3_scatter')

mean(df_ref_par3$ehf-df_eps_par3$ehf)
mean(abs(df_ref_par3$ehf-df_eps_par3$ehf))

df_ref = rbind(df_ref_par2b,df_ref_par3)
df_eps = rbind(df_eps_par2b,df_eps_par3)
ggplot(df_ref,aes(df_ref$ehf, df_eps$ehf)) +
  geom_point(alpha=.2) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1)) +
  ggtitle('Comparação EHF') +
  xlab('Parede Referência') +
  ylab('Parede Equivalente') +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(mean(abs(df_ref$ehf)-abs(df_eps$ehf)),4))) +
  annotate("text", x = .2, y = .8, label = paste("AE95 =",round(quantile((abs(df_ref$ehf)-abs(df_eps$ehf)),.95),4))) 
save_img('paredeeq_EHF_scatter')

mean(df_ref$ehf-df_eps$ehf)
mean(abs(df_ref$ehf-df_eps$ehf))
# LUPA!!!
df_maxdif = df_ref
df_maxdif$dif = df_ref$ehf-df_eps$ehf
df_maxdif$file[df_maxdif$dif == max(df_maxdif$dif)]
df_maxdif$zone[df_maxdif$dif == max(df_maxdif$dif)]
df_ref$ehf[df_ref$file == 'whole_ref_par2b_014']
df_eps$ehf[df_eps$file == 'whole_eq_par2b_014']

df_maxdif = subset(df_ref, df_ref$file == 'whole_ref_par2b_014')
df_maxdif = subset(df_maxdif, abs(df_maxdif$dif) > quantile((abs(df_ref$ehf)-abs(df_eps$ehf)),.95))
library(Hmisc)
hist.data.frame(df_maxdif)

lhs_values = c(
0.3743797,
0.5575577,
0.1659301,
0.4676304,
0.4468507,
0.7144547,
0.4426933,
0.5107219,
0.1674508,
0.427916,
0.4971307,
0.04757653,
0.7653883,
0.7422462,
0.3100196,
0.1650274)

lhs_names = colnames(df_maxdif)[8:23]

df_eqwallcomp = data.frame('parameter'=lhs_names,'value'=lhs_values)
ggplot(df_eqwallcomp,aes(df_eqwallcomp$parameter,df_eqwallcomp$value)) +
  geom_col() + ylim(c(0,1))

# HISTOGRAMAS
ggplot(df_dif,aes(df_dif$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('Diferenças no EHF') +
  xlab('EHF Referência - EHF Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = .05, y = 1000, label = paste("Média =",round(ehf_mean,5))) +
  annotate("text", x = .05, y = 1000*.9, label = paste("AE95 =",round(quantile(abs(df_dif$ehf),.95),4))) 
save_img('paredeeq_EHF')

ggplot(df_dif,aes(df_dif$temp)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças na Temperatura Operativa') +
  xlab('Temp. Referência - Temp. Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = -1, y = 1300, label = paste("Média =",round(temp_mean,3),'°C'))+
  annotate("text", x = -1, y = 1300*.9, label = paste("AE95 =",round(quantile(abs(df_dif$temp),.95),4),'°C'))
save_img('paredeeq_temp')

ggplot(df_dif,aes(df_dif$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH Referência - ACH Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = 1, y = 1700, label = paste("Média =",round(ach_mean,3),'ach'))
save_img('paredeeq_ACH')

# Par 1
ggplot(df_dif_par2a,aes(df_dif_par1$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('Diferenças no EHF Parede Concreto') +
  xlab('EHF Referência - EHF Parede equivalente') +
  ylab('Número de casos') #+
  annotate("text", x = .01, y = 550, label = paste("Média =",round(ehf_mean_par1,5))) +
  annotate("text", x = .01, y = 550*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par1$ehf),.95),4))) 
save_img('paredeeq_EHF_par1')

ggplot(df_dif_par1,aes(df_dif_par1$temp)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças na Temperatura Operativa Parede Concreto') +
  xlab('Temp. Referência - Temp. Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = -1, y = 300, label = paste("Média =",round(temp_mean_par1,3),'°C'))+
  annotate("text", x = -1, y = 300*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par1$temp),.95),4),'°C'))
save_img('paredeeq_temp_par1')

ggplot(df_dif_par1,aes(df_dif_par1$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH Parede Concreto') +
  xlab('ACH Referência - ACH Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = 1, y = 500, label = paste("Média =",round(ach_mean_par1,3),'ach'))
save_img('paredeeq_ACH_par1')

# Par 2a
ggplot(df_dif_par2a,aes(df_dif_par2a$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('Diferenças no EHF Parede Alvenaria CT Total') +
  xlab('EHF Referência - EHF Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = .05, y = 150, label = paste("Média =",round(ehf_mean_par2a,5))) +
  annotate("text", x = .05, y = 150*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par2a$ehf),.95),4))) 
save_img('paredeeq_EHF_par2a')

ggplot(df_dif_par2a,aes(df_dif_par2a$temp)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças na Temperatura Operativa Parede Alvenaria CT Total') +
  xlab('Temp. Referência - Temp. Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = -1, y = 300, label = paste("Média =",round(temp_mean_par2a,3),'°C'))+
  annotate("text", x = -1, y = 300*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par2a$temp),.95),4),'°C'))
save_img('paredeeq_temp_par2a')

ggplot(df_dif_par2a,aes(df_dif_par2a$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH Parede Alvenaria CT Total') +
  xlab('ACH Referência - ACH Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = 1, y = 500, label = paste("Média =",round(ach_mean_par2a,3),'ach'))
save_img('paredeeq_ACH_par2a')

# Par 2b
ggplot(df_dif_par2b,aes(df_dif_par2b$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('Diferenças no EHF Parede Alvenaria CT Metade') +
  xlab('EHF Referência - EHF Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = .05, y = 150, label = paste("Média =",round(ehf_mean_par2b,5))) +
  annotate("text", x = .05, y = 150*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par2b$ehf),.95),4))) 
save_img('paredeeq_EHF_par2b')

ggplot(df_dif_par2b,aes(df_dif_par2b$temp)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças na Temperatura Operativa Parede Alvenaria CT Metade') +
  xlab('Temp. Referência - Temp. Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = -1, y = 300, label = paste("Média =",round(temp_mean_par2b,3),'°C'))+
  annotate("text", x = -1, y = 300*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par2b$temp),.95),4),'°C'))
save_img('paredeeq_temp_par2b')

ggplot(df_dif_par2b,aes(df_dif_par2b$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH Parede Alvenaria CT Metade') +
  xlab('ACH Referência - ACH Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = 1, y = 500, label = paste("Média =",round(ach_mean_par2b,3),'ach'))
save_img('paredeeq_ACH_par2b')

# Par 3
ggplot(df_dif_par3,aes(df_dif_par3$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('Diferenças no EHF Parede Gesso + Isolamento') +
  xlab('EHF Referência - EHF Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = .05, y = 250, label = paste("Média =",round(ehf_mean_par3,5))) +
  annotate("text", x = .05, y = 250*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par3$ehf),.95),4))) 
save_img('paredeeq_EHF_par3')

ggplot(df_dif_par3,aes(df_dif_par3$temp)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças na Temperatura Operativa Parede Gesso + Isolamento') +
  xlab('Temp. Referência - Temp. Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = .5, y = 400, label = paste("Média =",round(temp_mean_par3,3),'°C'))+
  annotate("text", x = .5, y = 400*.9, label = paste("AE95 =",round(quantile(abs(df_dif_par3$temp),.95),4),'°C'))
save_img('paredeeq_temp_par3')

ggplot(df_dif_par3,aes(df_dif_par3$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH Parede Gesso + Isolamento') +
  xlab('ACH Referência - ACH Parede equivalente') +
  ylab('Número de casos') +
  annotate("text", x = 1, y = 500, label = paste("Média =",round(ach_mean_par3,3),'ach'))
save_img('paredeeq_ACH_par3')


df_ref = subset(df, substr(df$file,1,1) == 'r' &  df$temp_max < tempmax)  # refwall_par1

ggplot(df_ref,aes(df_ref$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.8, y = 30, label = paste("Média =",round(mean(df_ref$ehf),5))) +
  annotate("text", x = 0.8, y = 30*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf),.95),4))) 

ggplot(df_ref,aes(df_ref$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('ACH Referência') +
  xlab('ACH') +
  ylab('Número de casos') +
  annotate("text", x = 100, y = 60, label = paste("Média =",round(mean(df_ref$ach),2),'ach'))

# OUTDOORS x ADIABATIC ----

# df = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster0/means_cluster0.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster1/means_cluster1.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster2/means_cluster2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster3/means_cluster3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster4/means_cluster4.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster5/means_cluster5.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster6/means_cluster6.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster7/means_cluster7.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster8/means_cluster8.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/noafn/cluster9/means_cluster9.csv')
# )

df = read.csv('/media/marcelo/OS/dissertacao/single_zone/means_single_zone.csv')

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

temp_mean_out = mean(df_dif_out$temp)
temp_mean_adi = mean(df_dif_adi$temp)
ehf_mean_out = mean(df_dif_out$ehf)
ehf_mean_adi = mean(df_dif_adi$ehf)

dif_out_adi = df_dif_out$ehf - df_dif_adi$ehf
max(dif_out_adi)
min(dif_out_adi)  # erros sempre maiores no outdoors!

# ACH Cpeq SCATTERPLOT
ggplot(df_ref,aes(df_ref$ehf, df_adi$ehf)) +
  geom_point(alpha=.1) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1))

ggplot(df_ref,aes(df_ref$ehf, df_adi$ehf)) +
  geom_point(alpha=.15) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1)) +
  # ggtitle('Comparação EHF Adiabático') +
  xlab('Simulação detalhada - EHF (-)') +
  ylab('Parede adiabática - EHF (-)') +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(erro.medio(df_ref$ehf, df_adi$ehf),4))) +
  annotate("text", x = .2, y = .8, label = paste("AE95 =",round(erro.ae95(df_ref$ehf, df_adi$ehf),4)))
save_img('szadi_EHF_scatter')
mean(df_ref$ehf-df_adi$ehf)
mean(abs(df_ref$ehf-df_adi$ehf))
quantile(abs(df_ref$ehf-df_adi$ehf),.95)


ggplot(df_ref,aes(df_ref$ehf, df_out$ehf)) +
  geom_point(alpha=.15) +
  geom_abline() +
  xlim(c(0,1)) + ylim(c(0,1)) +
  # ggtitle('Comparação EHF Outdoors') +
  xlab('Simulação detalhada - EHF (-)') +
  ylab('Parede '~italic(outdoors)~' - EHF (-)') +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(erro.medio(df_ref$ehf, df_out$ehf),4))) +
  annotate("text", x = .2, y = .8, label = paste("AE95 =",round(erro.ae95(df_ref$ehf, df_out$ehf),4)))
save_img('szout_EHF_scatter')
mean(df_ref$ehf-df_out$ehf)
mean(abs(df_ref$ehf-df_out$ehf))
quantile(abs(df_ref$ehf-df_out$ehf),.95)

ggplot(df_dif_out,aes(df_dif_out$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('Diferenças no EHF Outdoors') +
  xlab('EHF Referência - EHF Singlezone') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 600, label = paste("Média =",round(ehf_mean_out,5))) +
  annotate("text", x = 0.2, y = 600*.9, label = paste("AE95 =",round(quantile(abs(df_dif_out$ehf),.95),4))) 
save_img('szout_EHF')

ggplot(df_dif_adi,aes(df_dif_adi$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('Diferenças no EHF Adiabático') +
  xlab('EHF Whole - EHF Singlezone') +
  ylab('Número de casos') +
  annotate("text", x = -.1, y = 1000, label = paste("Média =",round(ehf_mean_adi,5))) +
  annotate("text", x = -.1, y = 1000*.9, label = paste("AE95 =",round(quantile(abs(df_dif_adi$ehf),.95),4))) 
save_img('szadi_EHF')

ggplot(df_dif_out,aes(df_dif_out$temp)) +
  geom_histogram(binwidth = .05)+
  ggtitle('Diferenças de Temp. Operativa Outdoors') +
  xlab('Temp Referência - Temp Singlezone (°C)') +
  ylab('Número de casos') +
  annotate("text", x = -.25, y = 500, label = paste("Média =",round(temp_mean_out,5),'°C')) +
  annotate("text", x = -.25, y = 500*.9, label = paste("AE95 =",round(quantile(abs(df_dif_out$temp),.95),4),'°C')) 
save_img('szout_temp')

ggplot(df_dif_adi,aes(df_dif_adi$temp)) +
  geom_histogram(binwidth = .05)+
  ggtitle('Diferenças de Temp. Operativa Adiabático') +
  xlab('Temp Referência - Temp Singlezone (°C)') +
  ylab('Número de casos') +
  annotate("text", x = -1.1, y = 500, label = paste("Média =",round(temp_mean_adi,5),'°C')) +
  annotate("text", x = -1.1, y = 500*.9, label = paste("AE95 =",round(quantile(abs(df_dif_adi$temp),.95),4),'°C')) 
save_img('szadi_temp')


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

samp = read.csv('/media/marcelo/OS/dissertacao/sample_cpeq.csv')

df = read.csv('/media/marcelo/OS/dissertacao/cp_eq/means_cp_eq.csv')

# for(i in 0:3){
df_cpeq = subset(df, grepl(pattern = 'cp',df$file))  # substr(df$file,1,2) == 'cp')
df_noeq = subset(df, grepl(pattern = 'no',df$file))  # substr(df$file,1,2) == 'no')
df_ref = subset(df, grepl(pattern = 'whole',df$file))  # substr(df$file,1,1) == 'w')

df_noeq <- df_noeq[order(df_noeq$file),]
df_cpeq <- df_cpeq[order(df_cpeq$file),]
df_ref <- df_ref[order(df_ref$file),]

# ehfmin= .6+(i*.1)
# ehfmax = .7+(i*.1)
# df_ref2 = subset(df_ref, df_ref$ehf > ehfmin & df_ref$ehf < ehfmax)
# df_cpeq = subset(df_cpeq, df_ref$ehf > ehfmin & df_ref$ehf < ehfmax)
# df_noeq = subset(df_noeq, df_ref$ehf > ehfmin & df_ref$ehf < ehfmax)

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
# }

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
# CRACK ----
# 
# df = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster0/means_cluster0.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster1/means_cluster1.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster2/means_cluster2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster3/means_cluster3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster4/means_cluster4.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster5/means_cluster5.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster6/means_cluster6.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster7/means_cluster7.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster8/means_cluster8.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster9/means_cluster9.csv')
# )
# 
# df_2 = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster0/means_cluster0_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster1/means_cluster1_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster2/means_cluster2_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster3/means_cluster3_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster4/means_cluster4_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster5/means_cluster5_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster6/means_cluster6_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster7/means_cluster7_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster8/means_cluster8_2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster9/means_cluster9_2.csv')
# )
# 
# df_3 = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster0/means_cluster0_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster1/means_cluster1_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster2/means_cluster2_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster3/means_cluster3_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster4/means_cluster4_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster5/means_cluster5_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster6/means_cluster6_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster7/means_cluster7_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster8/means_cluster8_3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster9/means_cluster9_3.csv')
# )
# 
# df_015 = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster0/015means_cluster0.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster1/015means_cluster1.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster2/015means_cluster2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster3/015means_cluster3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster4/015means_cluster4.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster5/015means_cluster5.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster6/015means_cluster6.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster7/015means_cluster7.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster8/015means_cluster8.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/crack/cluster9/015means_cluster9.csv')
# )

samp = read.csv('/media/marcelo/OS/dissertacao/sample_cpeq.csv')
df = read.csv('/media/marcelo/OS/dissertacao/cp_eq/means_cp_eq.csv')
df_noeq = read.csv('/media/marcelo/OS/dissertacao/cp_eq_extra_noeq/means_cp_eq_extra_noeq.csv') # 10, 30, 50, 70, 90, 99

samp = read.csv('/media/marcelo/OS/dissertacao/sample_cpeq.csv')
df = read.csv('/media/marcelo/OS/dissertacao/cp_eq/means_cp_eq.csv')
df_ref = subset(df, grepl(pattern = 'whole',df$file))  # substr(df$file,1,1) == 'w')  # & df$ehf < .9)
df_ref = cbind(df_ref, samp)

df = read.csv('/media/marcelo/OS/dissertacao/cp_eq_extra/means_cp_eq_extra.csv')
df_cp_040 = subset(df, grepl(pattern = '_cpeq_40_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_cp_045 = subset(df, grepl(pattern = '_cpeq_45_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_no_040 = subset(df, grepl(pattern = '_noeq_40_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_no_045 = subset(df, grepl(pattern = '_noeq_45_',df$file))  # substr(df$file,1,10) == '050crack_c')  # & df_ref$ehf < .9)

df = read.csv('/media/marcelo/OS/dissertacao/cp_eq_extra2/means_cp_eq_extra2.csv')
df_cp_060 = subset(df, grepl(pattern = '_cpeq_60_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_cp_055 = subset(df, grepl(pattern = '_cpeq_55_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_no_060 = subset(df, grepl(pattern = '_noeq_60_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_no_055 = subset(df, grepl(pattern = '_noeq_55_',df$file))  # substr(df$file,1,10) == '050crack_c')  # & df_ref$ehf < .9)

df = read.csv('/media/marcelo/OS/dissertacao/cp_eq_extra3/means_cp_eq_extra3.csv')
df_cp_070 = subset(df, grepl(pattern = '_cpeq_70_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_cp_080 = subset(df, grepl(pattern = '_cpeq_80_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_no_070 = subset(df, grepl(pattern = '_noeq_70_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_no_080 = subset(df, grepl(pattern = '_noeq_80_',df$file))  # substr(df$file,1,10) == '050crack_c')  # & df_ref$ehf < .9)

df = read.csv('/media/marcelo/OS/dissertacao/cp_eq_extra4/means_cp_eq_extra4.csv')
df_cp_090 = subset(df, grepl(pattern = '_cpeq_90_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_cp_095 = subset(df, grepl(pattern = '_cpeq_95_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_cp_099 = subset(df, grepl(pattern = '_cpeq_99_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)

df_ref = subset(df, grepl(pattern = 'whole',df$file))  # substr(df$file,1,1) == 'w')  # & df$ehf < .9)
df_ref = cbind(df_ref, samp)
# df_001 = subset(df, substr(df$file,1,3) == '001')  # & df_ref$ehf < .9)
df_cp_010 = subset(df, grepl(pattern = '_cpeq_10_',df$file))  # substr(df$file,1,10) == '010crack_c')  # & df_ref$ehf < .9)  # 
df_cp_015 = subset(df, grepl(pattern = '_cpeq_15_',df$file))  # substr(df_015$file,1,10) == '015crack_c')  # & df_ref$ehf < .9)  # 
df_cp_020 = subset(df, grepl(pattern = '_cpeq_20_',df$file))  # substr(df$file,1,10) == '020crack_c')  # & df_ref$ehf < .9)
df_cp_030 = subset(df, grepl(pattern = '_cpeq_30_',df$file))  # substr(df$file,1,10) == '030crack_c')  # & df_ref$ehf < .9)
df_cp_040 = subset(df, grepl(pattern = '_cpeq_40_',df$file))  # substr(df$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_cp_050 = subset(df, grepl(pattern = '_cpeq_50_',df$file))  # substr(df_noeq$file,1,10) == '050crack_c')  # & df_ref$ehf < .9)
df_no_010 = subset(df_noeq, grepl(pattern = '_noeq_10_',df_noeq$file))  # substr(df_noeq$file,1,10) == '010crack_c')  # & df_ref$ehf < .9)  # 
df_no_015 = subset(df_noeq, grepl(pattern = '_noeq_15_',df_noeq$file))  # substr(df_015$file,1,10) == '015crack_c')  # & df_ref$ehf < .9)  # 
df_no_020 = subset(df_noeq, grepl(pattern = '_noeq_20_',df_noeq$file))  # substr(df_noeq$file,1,10) == '020crack_c')  # & df_ref$ehf < .9)
df_no_030 = subset(df_noeq, grepl(pattern = '_noeq_30_',df_noeq$file))  # substr(df_noeq$file,1,10) == '030crack_c')  # & df_ref$ehf < .9)
df_no_040 = subset(df_noeq, grepl(pattern = '_noeq_40_',df_noeq$file))  # substr(df_noeq$file,1,10) == '040crack_c')  # & df_ref$ehf < .9)
df_no_050 = subset(df_noeq, grepl(pattern = '_noeq_50_',df_noeq$file))  # substr(df_noeq$file,1,10) == '050crack_c')  # & df_ref$ehf < .9)
df_no_070 = subset(df_noeq, grepl(pattern = '_noeq_70_',df_noeq$file))  # substr(df_noeq$file,1,10) == '070crack_c')  # & df_ref$ehf < .9)
df_no_090 = subset(df_noeq, grepl(pattern = '_noeq_90_',df_noeq$file))  # substr(df_noeq$file,1,10) == '090crack_c')  # & df_ref$ehf < .9)
df_no_099 = subset(df_noeq, grepl(pattern = '_noeq_99_',df_noeq$file))  # substr(df_noeq$file,1,10) == '099crack_c')  # & df_ref$ehf < .9)

df_cpeq = rbind(df_cp_010,df_cp_020,df_cp_030,df_cp_040,df_cp_045,df_cp_050,df_cp_055,df_cp_060,
                df_cp_070,df_cp_080,df_cp_090,df_cp_095,df_cp_099)
df_noeq = rbind(df_no_010,df_no_020,df_no_030,df_no_040,df_no_045,df_no_050,df_no_055,df_no_060,
                df_no_070,df_no_080,df_no_090,df_no_099)

Cqs = c('10','30','40','45','50','55','60','70','80','90','99')
cq_compare = data.frame('Method'=rep(NA,2*length(Cqs)),'Cq'=rep(NA,2*length(Cqs)),
                        'RMSE'=rep(NA,2*length(Cqs)),'mean'=rep(NA,2*length(Cqs)),'abs_mean'=rep(NA,2*length(Cqs)),'AE95'=rep(NA,2*length(Cqs)),
                        'RMSE_ehf'=rep(NA,2*length(Cqs)),'mean_ehf'=rep(NA,2*length(Cqs)),'abs_mean_ehf'=rep(NA,2*length(Cqs)),'AE95_ehf'=rep(NA,2*length(Cqs)))
line=1
for(Cq in Cqs){
  sub_cpeq = subset(df_cpeq,grepl(pattern = paste('_cpeq_',Cq,sep=''),df_cpeq$file))
  sub_noeq = subset(df_noeq,grepl(pattern = paste('_noeq_',Cq,sep=''),df_noeq$file))
  
  cq_compare$Method[line] = 'Cp equivalente'
  cq_compare$Cq[line] = Cq
  cq_compare$RMSE[line] = (sum((sub_cpeq$ach-df_ref$ach)**2)/nrow(df_ref))**(1/2)
  cq_compare$mean[line] = mean(sub_cpeq$ach-df_ref$ach)
  cq_compare$abs_mean[line] = mean(abs(sub_cpeq$ach-df_ref$ach))
  cq_compare$AE95[line] = quantile(abs(sub_cpeq$ach-df_ref$ach),.95)
  cq_compare$RMSE_ehf[line] = (sum((sub_cpeq$ehf-df_ref$ehf)**2)/nrow(df_ref))**(1/2)
  cq_compare$mean_ehf[line] = mean(sub_cpeq$ehf-df_ref$ehf)
  cq_compare$abs_mean_ehf[line] = mean(abs(sub_cpeq$ehf-df_ref$ehf))
  cq_compare$AE95_ehf[line] = quantile(abs(sub_cpeq$ehf-df_ref$ehf),.95)
  
  cq_compare$Method[line+1] = 'Cp método analítico'
  cq_compare$Cq[line+1] = Cq
  cq_compare$RMSE[line+1] = (sum((sub_noeq$ach-df_ref$ach)**2)/nrow(df_ref))**(1/2)
  cq_compare$mean[line+1] = mean(sub_noeq$ach-df_ref$ach)
  cq_compare$abs_mean[line+1] = mean(abs(sub_noeq$ach-df_ref$ach))
  cq_compare$AE95[line+1] = quantile(abs(sub_noeq$ach-df_ref$ach),.95)
  cq_compare$RMSE_ehf[line+1] = (sum((sub_noeq$ehf-df_ref$ehf)**2)/nrow(df_ref))**(1/2)
  cq_compare$mean_ehf[line+1] = mean(sub_noeq$ehf-df_ref$ehf)
  cq_compare$abs_mean_ehf[line+1] = mean(abs(sub_noeq$ehf-df_ref$ehf))
  cq_compare$AE95_ehf[line+1] = quantile(abs(sub_noeq$ehf-df_ref$ehf),.95)
  
  # print (paste('Cp EQ',Cq))
  # print(((sum((sub_cpeq$ach-df_ref$ach)**2))**(1/2))/nrow(df_ref))
  # print (paste('Cp NO',Cq))
  # print(((sum((sub_noeq$ach-df_ref$ach)**2))**(1/2))/nrow(df_ref))
  line = line + 2
}

cq_compare$Cq_num = as.numeric(cq_compare$Cq)/100
cq_compare$Cq_num[cq_compare$Cq_num == .99] = 1

names(cq_compare)[names(cq_compare)=="Method"]  <- "Método"
names(cq_compare)[names(cq_compare)=="Cq_num"]  <- "Coeficiente de fluxo\n(kg/sPa^n em 1 Pa)"
ggplot(cq_compare,aes(cq_compare$RMSE,cq_compare$RMSE_ehf,shape=`Método`)) +
  geom_point(size = 3, aes(col=`Coeficiente de fluxo\n(kg/sPa^n em 1 Pa)`)) +
  xlab('RMSE ACH') + ylab('RMSE EHF') +
  annotate("text", x = cq_compare$RMSE[cq_compare$Método == 'Cp equivalente' & cq_compare$Cq == '80'],
           y = cq_compare$RMSE_ehf[cq_compare$Método == 'Cp equivalente' & cq_compare$Cq == '80'], colour = "red",label='X',size =7)
save_img('cpeq_pareto',fact = 1)

ggplot(df_cp_080,aes(df_ref$ach, df_cp_080$ach)) +
    geom_point(alpha=.31) +
    geom_abline() +
    xlim(c(0,140)) + ylim(c(0,140))  +
    xlab('Modelo detalhado\nmédia anual de trocas de ar (ACH)') +
    ylab('Modelo simplificado\nmédia anual de trocas de ar (ACH)') +
    annotate("text", x = 50, y = 135, label = paste("Erro médio =",round(erro.medio(df_ref$ach, df_cp_080$ach),2),'ACH')) +
    annotate("text", x = 45, y = 125, label = paste("AE95 =",round(erro.ae95(df_ref$ach, df_cp_080$ach),2),'ACH'))
save_img(('cpeq_COM_80'),square = TRUE)

ggplot(df_cp_080,aes(df_ref$ehf, df_cp_080$ehf)) +
    geom_point(alpha=.1) +
    geom_abline() +
    xlim(c(0,1)) + ylim(c(0,1))  +
    xlab('Modelo detalhado - EHF (-)') +
    ylab('Modelo simplificado - EHF (-)') +
    annotate("text", x = .25, y = .95, label = paste("Erro médio =",round(erro.medio(df_ref$ehf, df_cp_080$ehf),4))) +
    annotate("text", x = .21, y = .85, label = paste("AE95 =",round(erro.ae95(df_ref$ehf, df_cp_080$ehf),4)))
save_img(('cpeq_COM_80EHF'),square = TRUE)
  
# threshold = .8
# 
# df_ref = subset(df_ref, df_ref$ehf < threshold)
# threshold = .7
# df_cp_010 = subset(df, substr(df$file,1,10) == '010crack_c' & df_ref$ehf < threshold)  # )
# tempmax = 40
# df_cp_010 = subset(df, substr(df$file,1,10) == '010crack_c' & df_ref$temp_max < tempmax)  # )
# peop = .8
# df_cp_010 = subset(df, substr(df$file,1,10) == '010crack_c' & df_ref$people < peop)  # )

df_ref_cor = df_ref
cor_matrix_1 = cor(df_ref_cor[,c("temp","ach","ehf","area",
                                 "ratio","zone_height", "azimuth","absorptance", 
                                 "wwr","people",'open_fac', 'corner_window')])

corrplot.mixed(cor_matrix_1, lower = "number", upper = "ellipse",
               tl.pos = "lt", number.cex = 0.6, bg = "black",
               tl.col = "black", tl.srt = 90, tl.cex = 0.8)
# PLOTS
infiltrations = unique(substr(df_noeq$file,13,14))
for (inf in infiltrations){
  dfplot = subset(df_noeq, substr(df_noeq$file,13,14) == inf)
  ggplot(df_ref,aes(df_ref$ach, dfplot$ach)) +
    geom_point(alpha=.1) +
    geom_abline() +
    xlim(c(0,140)) + ylim(c(0,140))  +
    ggtitle(paste('Comparação ACH SEM Cp eq inf = 0.',inf,sep='')) +
    xlab('Referência (ACH)') +
    ylab('Crack (ACH)') +
    annotate("text", x = 20, y = 120, label = paste("Dif. abs. média =",round(mean(abs(df_ref$ach-dfplot$ach)),2))) +
    annotate("text", x = 20, y = 110, label = paste("AE95 =",round(quantile((abs(df_ref$ach-dfplot$ach)),.95),2)))
  save_img(paste('cpeq_SEM_',inf,sep=''),fact = 1.25)
  dfplot = subset(df_cpeq, substr(df_cpeq$file,13,14) == inf)
  ggplot(df_ref,aes(df_ref$ach, dfplot$ach)) +
    geom_point(alpha=.1) +
    geom_abline() +
    xlim(c(0,140)) + ylim(c(0,140))  +
    ggtitle(paste('Comparação ACH COM Cp eq inf = 0.',inf,sep='')) +
    xlab('Referência (ACH)') +
    ylab('Crack (ACH)') +
    annotate("text", x = 20, y = 120, label = paste("Dif. abs. média =",round(mean(abs(df_ref$ach-dfplot$ach)),2))) +
    annotate("text", x = 20, y = 110, label = paste("AE95 =",round(quantile((abs(df_ref$ach-dfplot$ach)),.95),2))) 
  save_img(paste('cpeq_COM_',inf,sep=''),fact = 1.25)
  ggplot(df_ref,aes(df_ref$ehf, dfplot$ehf)) +
    geom_point(alpha=.25) +
    geom_abline() +
    xlim(c(0,1)) + ylim(c(0,1))  +
    ggtitle(paste('Comparação EHF COM Cp eq inf = 0.',inf,sep='')) +
    xlab('Referência (EHF)') +
    ylab('Crack (EHF)') +
    annotate("text", x = .2, y = .95, label = paste("Média =",round(mean(df_ref$ehf-dfplot$ehf),4))) +
    annotate("text", x = .2, y = .875, label = paste("Dif. abs. média =",round(mean(abs(df_ref$ehf-dfplot$ehf)),4))) +
    annotate("text", x = .20, y = .8, label = paste("AE95 =",round(quantile((abs(df_ref$ehf-dfplot$ehf)),.95),4))) 
  save_img(paste('cpeq_COM_',inf,'EHF',sep=''),fact = 1.25)
}

# só CP equivalente
infiltrations= c('40', '45', '55','60','80','95')
for (inf in infiltrations){
  dfplot = subset(df_cpeq, substr(df_cpeq$file,13,14) == inf)
  ggplot(df_ref,aes(df_ref$ach, dfplot$ach)) +
    geom_point(alpha=.1) +
    geom_abline() +
    xlim(c(0,140)) + ylim(c(0,140))  +
    ggtitle(paste('Comparação ACH COM Cp eq inf = 0.',inf,sep='')) +
    xlab('Referência (ACH)') +
    ylab('Crack (ACH)') +
    annotate("text", x = 20, y = 120, label = paste("Dif. abs. média =",round(mean(abs(df_ref$ach-dfplot$ach)),2))) +
    annotate("text", x = 20, y = 110, label = paste("AE95 =",round(quantile((abs(df_ref$ach-dfplot$ach)),.95),2))) 
  save_img(paste('cpeq_COM_',inf,sep=''),fact = 1.25)
  ggplot(df_ref,aes(df_ref$ehf, dfplot$ehf)) +
    geom_point(alpha=.25) +
    geom_abline() +
    xlim(c(0,1)) + ylim(c(0,1))  +
    ggtitle(paste('Comparação EHF COM Cp eq inf = 0.',inf,sep='')) +
    xlab('Referência (EHF)') +
    ylab('Crack (EHF)') +
    annotate("text", x = .2, y = .95, label = paste("Média =",round(mean(df_ref$ehf-dfplot$ehf),4))) +
    annotate("text", x = .2, y = .875, label = paste("Dif. abs. média =",round(mean(abs(df_ref$ehf-dfplot$ehf)),4))) +
    annotate("text", x = .20, y = .8, label = paste("AE95 =",round(quantile((abs(df_ref$ehf-dfplot$ehf)),.95),4))) 
  save_img(paste('cpeq_COM_',inf,'EHF',sep=''),fact = 1.25)
}

df_x = subset(df_ref, df_ref$open_fac < .5)
df_cp_080x = subset(df_cp_080, df_ref$open_fac < .5)
# ACH Cpeq SCATTERPLOT
# ggplot(df_ref,aes(df_ref$ehf, df_cp_099$ehf)) +
ggplot(df_ref,aes(df_ref$ach, df_cp_080$ach)) +
# ggplot(df_x,aes(df_x$ach, df_cp_080x$ach)) +
  geom_point(alpha=.1) +
  geom_abline() +
  # xlim(c(0,1)) + ylim(c(0,1))  # EHF
  xlim(c(0,140)) + ylim(c(0,140))  # ACH

ggplot((df_ref),aes(df_ref$ach-df_cp_010$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 010') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_010$ach),3),'ach'))

ggplot((df_ref),aes(df_ref$ach-df_cp_015$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 015') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_015$ach),3),'ach'))


ggplot((df_ref),aes(df_ref$ach-df_cp_020$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 020') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_020$ach),3),'ach'))


ggplot((df_ref),aes(df_ref$ach-df_cp_030$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 030') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_030$ach),3),'ach'))


ggplot((df_ref),aes(df_ref$ach-df_cp_040$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 040') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_040$ach),3),'ach'))


df_ref_backup = df_ref
df_cp_050_backup = df_cp_050
df_ref = subset(df_ref, df_ref_backup$ehf < .5)
df_cp_050 = subset(df_cp_050, df_ref_backup$ehf < .5)
ggplot((df_ref),aes(df_ref$ach-df_cp_050$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 050') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_050$ach),3),'ach'))
df_ref = df_ref_backup
df_cp_050 = df_cp_050_backup

# ACH NOeq

ggplot((df_ref),aes(df_ref$ach-df_no_010$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 010') +
  xlab('ACH Referência - ACH NOeq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_no_010$ach),3),'ach'))


ggplot((df_ref),aes(df_ref$ach-df_no_020$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 020') +
  xlab('ACH Referência - ACH NOeq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_no_020$ach),3),'ach'))


ggplot((df_ref),aes(df_ref$ach-df_no_030$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 030') +
  xlab('ACH Referência - ACH NOeq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_no_030$ach),3),'ach'))


ggplot((df_ref),aes(df_ref$ach-df_no_040$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 040') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_no_040$ach),3),'ach'))


ggplot((df_ref),aes(df_ref$ach-df_no_050$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 050') +
  xlab('ACH Referência - ACH no_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_no_050$ach),3),'ach'))

# EHF Cpeq

ggplot((df_ref),aes(df_ref$ehf-df_cp_010$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_cp_010$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_010$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_cp_010$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_010$ehf),.95),4)))


ggplot((df_ref),aes(df_ref$ehf-df_cp_015$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 015') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_cp_010$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_010$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_cp_015$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_015$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_cp_020$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_cp_020$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_020$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_cp_020$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_020$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_cp_030$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.30') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_cp_030$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_030$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_cp_030$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_030$ehf),.95),4)))

df_ref_backup = df_ref
df_cp_050_backup = df_cp_050
df_ref = subset(df_ref, df_ref_backup$ehf < .75)
df_cp_050 = subset(df_cp_050, df_ref_backup$ehf < .75)
ggplot((df_ref),aes(df_ref$ehf-df_cp_050$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF CpEq 0.70') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = -0.15, y = 60, label = paste("Média =",round(mean(df_ref$ehf-df_cp_050$ehf),5))) +
  annotate("text", x = -0.15, y = 60*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_050$ehf),.95),4)))
  # annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_cp_050$ehf),5))) +
  # annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_050$ehf),.95),4)))
df_ref = df_ref_backup
df_cp_050 = df_cp_050_backup

# EHF NOeq

ggplot((df_ref),aes(df_ref$ehf-df_no_010$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF NoEq 0.10') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_no_010$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_010$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_no_010$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_010$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_020$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_no_020$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_020$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_no_020$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_020$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_030$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF NoEq 0.30') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_no_030$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_030$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_no_030$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_030$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_050$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF NoEq 0.50') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_no_050$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_050$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_no_050$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_050$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_070$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF NoEq 0.70') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_no_070$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_070$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_no_070$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_070$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_090$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF NoEq 0.90') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_no_090$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_090$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_no_090$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_090$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_099$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF NoEq 1.0') +
  xlab('EHF') +
  ylab('Número de casos') +
  # annotate("text", x = -0.15, y = 5, label = paste("Média =",round(mean(df_ref$ehf-df_no_099$ehf),5))) +
  # annotate("text", x = -0.15, y = 4.5*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_099$ehf),.95),4)))
  annotate("text", x = -0.15, y = 70, label = paste("Média =",round(mean(df_ref$ehf-df_no_099$ehf),5))) +
  annotate("text", x = -0.15, y = 70*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_099$ehf),.95),4)))

faixa_ehf = c('df_ref_backup$ehf < .5',
              'df_ref_backup$ehf > .5 &  df_ref_backup$ehf < .75',
              'df_ref_backup$ehf > .75',
              'df_ref_backup$ehf < .75')

# 0.40 e 0.45

# EHF NoEq
ggplot((df_ref),aes(df_ref$ehf-df_no_040$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.40') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_no_040$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_040$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_045$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.45') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_no_045$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_045$ehf),.95),4)))

# EHF CpEq
ggplot((df_ref),aes(df_ref$ehf-df_cp_040$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.40') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_040$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_040$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_cp_045$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.45') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_045$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_045$ehf),.95),4)))

# 0.55 e 0.60

# EHF NoEq
ggplot((df_ref),aes(df_ref$ehf-df_no_060$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.60') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_no_060$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_060$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_055$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.55') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_no_055$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_055$ehf),.95),4)))

# EHF CpEq
df_ref_backup = df_ref
df_cp_060_backup = df_cp_060
df_ref = subset(df_ref, faixa_ehf[1])
df_cp_060 = subset(df_cp_060, faixa_ehf[1])
ggplot((df_ref),aes(df_ref$ehf-df_cp_060$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.60 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_060$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_060$ehf),.95),4)))
df_ref = df_ref_backup
df_cp_060 = df_cp_060_backup

df_ref_backup = df_ref
df_cp_055_backup = df_cp_055
df_ref = subset(df_ref, faixa_ehf[1])
df_cp_055 = subset(df_cp_055, faixa_ehf[1])
ggplot((df_ref),aes(df_ref$ehf-df_cp_055$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.55 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_055$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_055$ehf),.95),4)))
df_ref = df_ref_backup
df_cp_055 = df_cp_055_backup

# ACH 
ggplot((df_ref),aes(df_ref$ach-df_cp_055$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 055') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_055$ach),3),'ach'))

ggplot((df_ref),aes(df_ref$ach-df_cp_060$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 060') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_060$ach),3),'ach'))

# 0.7 e 0.80

# EHF NoEq
ggplot((df_ref),aes(df_ref$ehf-df_no_070$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.70') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_no_070$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_070$ehf),.95),4)))

ggplot((df_ref),aes(df_ref$ehf-df_no_080$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.80') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_no_080$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_no_080$ehf),.95),4)))

# EHF CpEq
df_ref_backup = df_ref
df_cp_070_backup = df_cp_070
df_ref = subset(df_ref, faixa_ehf[1])
df_cp_070 = subset(df_cp_070, faixa_ehf[1])
ggplot((df_ref),aes(df_ref$ehf-df_cp_070$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.70 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_070$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_070$ehf),.95),4)))
df_ref = df_ref_backup
df_cp_070 = df_cp_070_backup

df_ref_backup = df_ref
df_cp_080_backup = df_cp_080
df_ref = subset(df_ref, df_ref_backup$ehf < .75)
df_cp_080 = subset(df_cp_080, df_ref_backup$ehf < .75)
ggplot((df_ref),aes(df_ref$ehf-df_cp_080$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.80 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_080$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_080$ehf),.95),4)))
df_ref = df_ref_backup
df_cp_080 = df_cp_080_backup

df_ref_backup = df_ref
df_cp_080_backup = df_cp_080
df_ref = subset(df_ref, df_ref_backup$ehf < .75)
df_cp_080 = subset(df_cp_080, df_ref_backup$ehf < .75)
ggplot((df_ref),aes(df_ref$temp-df_cp_080$temp)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.80 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$temp-df_cp_080$temp),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$temp-df_cp_080$temp),.95),4)))
df_ref = df_ref_backup
df_cp_080 = df_cp_080_backup

# ACH 
ggplot((df_ref),aes(df_ref$ach-df_cp_080$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 080') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_080$ach),3),'ach'))

ggplot((df_ref),aes(df_ref$ach-df_cp_070$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 070') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_070$ach),3),'ach'))

# 0.9 e 0.95 e 1.00

# EHF CpEq
df_ref_backup = df_ref
df_cp_090_backup = df_cp_090
df_ref = subset(df_ref, df_ref_backup$ehf < .75)
df_cp_090 = subset(df_cp_090, df_ref_backup$ehf < .75)
ggplot((df_ref),aes(df_ref$ehf-df_cp_090$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.90 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_090$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.93, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_090$ehf),.95),4)))
df_ref = df_ref_backup
df_cp_090 = df_cp_090_backup

df_ref_backup = df_ref
df_cp_095_backup = df_cp_095
df_ref = subset(df_ref, df_ref_backup$ehf < .75)
df_cp_095 = subset(df_cp_095, df_ref_backup$ehf < .75)
ggplot((df_ref),aes(df_ref$ehf-df_cp_095$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.95 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_095$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$ehf-df_cp_095$ehf),.95),4)))
df_ref = df_ref_backup
df_cp_095 = df_cp_095_backup

df_ref_backup = df_ref
df_cp_099_backup = df_cp_099
df_ref = subset(df_ref, df_ref_backup$ehf < .75)
df_cp_099 = subset(df_cp_099, df_ref_backup$ehf < .75)
ggplot((df_ref),aes(df_ref$ehf-df_cp_099$ehf)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.99 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$ehf-df_cp_099$ehf),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE99 =",round(quantile(abs(df_ref$ehf-df_cp_099$ehf),.99),4)))
df_ref = df_ref_backup
df_cp_099 = df_cp_099_backup

df_ref_backup = df_ref
df_cp_095_backup = df_cp_095
df_ref = subset(df_ref, df_ref_backup$ehf < .75)
df_cp_095 = subset(df_cp_095, df_ref_backup$ehf < .75)
ggplot((df_ref),aes(df_ref$temp-df_cp_095$temp)) +
  geom_histogram(binwidth = .005)+
  ggtitle('EHF Referência 0.95 - 0.50-0.75') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.2, y = 45, label = paste("Média =",round(mean(df_ref$temp-df_cp_095$temp),5))) +
  annotate("text", x = 0.2, y = 45*.9, label = paste("AE95 =",round(quantile(abs(df_ref$temp-df_cp_095$temp),.95),4)))
df_ref = df_ref_backup
df_cp_095 = df_cp_095_backup

# ACH 
ggplot((df_ref),aes(df_ref$ach-df_cp_080$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 080') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_080$ach),3),'ach'))

ggplot((df_ref),aes(df_ref$ach-df_cp_090$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 090') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_090$ach),3),'ach'))

ggplot((df_ref),aes(df_ref$ach-df_cp_095$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 095') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_095$ach),3),'ach'))

ggplot((df_ref),aes(df_ref$ach-df_cp_099$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH 1.0') +
  xlab('ACH Referência - ACH Cp_eq') +
  ylab('Número de casos') +
  # ylim(c(0,1100)) +
  annotate("text", x = 2, y = 200, label = paste("Média =",round(mean(df_ref$ach-df_cp_099$ach),3),'ach'))

# EHF GERAL

ggplot(df_ref,aes(df_ref$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('EHF Referência') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.4, y = 60, label = paste("Média =",round(mean(df_ref$ehf),5))) +
  annotate("text", x = 0.4, y = 60*.9, label = paste("percentil 95% =",round(quantile(abs(df_ref$ehf),.95),4)))

ggplot(df_cp_050,aes(df_cp_050$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('EHF 0.50') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.4, y = 60, label = paste("Média =",round(mean(df_cp_050$ehf),5))) +
  annotate("text", x = 0.4, y = 60*.9, label = paste("percentil 95% =",round(quantile(abs(df_cp_050$ehf),.95),4)))

ggplot(df_cp_080,aes(df_cp_080$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('EHF 0.80') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.4, y = 60, label = paste("Média =",round(mean(df_cp_080$ehf),5))) +
  annotate("text", x = 0.4, y = 60*.9, label = paste("percentil 95% =",round(quantile(abs(df_cp_080$ehf),.95),4)))

ggplot(df_cp_060,aes(df_cp_060$ehf)) +
  geom_histogram(binwidth = .01)+
  ggtitle('EHF 0.60') +
  xlab('EHF') +
  ylab('Número de casos') +
  annotate("text", x = 0.4, y = 60, label = paste("Média =",round(mean(df_cp_060$ehf),5))) +
  annotate("text", x = 0.4, y = 60*.9, label = paste("percentil 95% =",round(quantile(abs(df_cp_060$ehf),.95),4)))

# CRACK - coisas antigas ----
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

samp = read.csv('/media/marcelo/OS/dissertacao/sample_crack.csv')
samp = samp[rep(seq_len(nrow(samp)), each=6),]
df_ref_cor = cbind(df_ref, samp)
df_ref_cor = df_ref_cor[df_ref_cor$temp_max < 40,]
df_ref_cor = df_ref_cor[df_ref_cor$people < .8,]

cor_matrix_1 = cor(df_ref_cor[,c("temp","temp_max","ach","ehf","area",
                                   "ratio","zone_height", "azimuth","absorptance", 
                                   "wwr","people",'open_fac', 'zone')])

corrplot.mixed(cor_matrix_1, lower = "number", upper = "ellipse",
               tl.pos = "lt", number.cex = 0.6, bg = "black",
               tl.col = "black", tl.srt = 90, tl.cex = 0.8)


# ---- epw ----

months = c('Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro',
           'Outubro','Novembro','Dezembro')

means = c(21.16,22.35,21.67,20.76,17.45,16.77,17.34,18.28,17.68,
          20.51,20.15,20.87)
# month_means = read.csv('~/dissertacao/ehf/month_means_8760.csv')
# unique(month_means$mean_temp)

sp_means = data.frame('Meses'=months,'Temperatura.media'=means)
sp_means$T_sup = 17.8+3.5 + .31* sp_means$Temperatura.media

epw = read.csv('/media/marcelo/OS/LabEEE_1-2/idf-creator/epw_sp.epw',skip=8,header = FALSE)
mean(epw$V7[epw$V2 == 1])
epw$mean.temp[epw$V2 == 1] = mean(epw$V7[epw$V2 == 1])
epw$mean.temp[epw$V2 == 2] = mean(epw$V7[epw$V2 == 2])
epw$mean.temp[epw$V2 == 3] = mean(epw$V7[epw$V2 == 3])
epw$mean.temp[epw$V2 == 4] = mean(epw$V7[epw$V2 == 4])
epw$mean.temp[epw$V2 == 5] = mean(epw$V7[epw$V2 == 5])
epw$mean.temp[epw$V2 == 6] = mean(epw$V7[epw$V2 == 6])
epw$mean.temp[epw$V2 == 7] = mean(epw$V7[epw$V2 == 7])
epw$mean.temp[epw$V2 == 8] = mean(epw$V7[epw$V2 == 8])
epw$mean.temp[epw$V2 == 9] = mean(epw$V7[epw$V2 == 9])
epw$mean.temp[epw$V2 == 10] = mean(epw$V7[epw$V2 == 10])
epw$mean.temp[epw$V2 == 11] = mean(epw$V7[epw$V2 == 11])
epw$mean.temp[epw$V2 == 12] = mean(epw$V7[epw$V2 == 12])
unique(epw$mean.temp)

epw$t.sup = 17.8+3.5 + .31* epw$mean.temp
epw$t.inf = 17.8-3.5 + .31* epw$mean.temp
unique(epw$t.sup)

epw$data = paste(epw$V2,epw$V3,epw$V4)
epw$data <- as.POSIXct(strptime(epw$data,"%m %d %H"),format = "%m/%d/%H")

library(scales)

cols = c('Temperatura\nbulbo seco\nexterna' = 'gray','Média mensal\ntemperatura\nexterna' = 'black','Limite superior\ntemperatura\noperativa' = 'red',
         'Limite inferior\ntemperatura\noperativa' = 'blue')

ggplot(epw,aes(epw$data,epw$V7))+
  geom_line(aes(col='Temperatura\nbulbo seco\nexterna'))+
  geom_line(aes(epw$data,epw$mean.temp,col='Média mensal\ntemperatura\nexterna'))+
  geom_line(aes(epw$data,epw$t.sup,col='Limite superior\ntemperatura\noperativa')) +
  geom_line(aes(epw$data,epw$t.inf,col='Limite inferior\ntemperatura\noperativa')) +
  scale_x_datetime(labels = date_format("%B")) +
  scale_colour_manual(name=NULL, values=cols) +
  ylab('Temperatura (°C)') +
  xlab(NULL) +
  theme(legend.position="bottom")
save_img('temp_means', fact=.8)
  
# January & 21,16 & 28.66 \\
# February & 22,35 & 29.03 \\\hline
# March & 21,67 & 28.82 \\\hline
# April & 20,76 & 28.54 \\\hline
# May & 17,45 & 27.51 \\\hline
# June & 16,77 & 27.30 \\hline
# July & 17,34 & 27.48 \\hline
# August & 18,28 & 27.77\hline
# September & 17,68 & 27.58 \\\hline
# October & 20,51 & 28.46 \\\hline
# November & 20,15 & 28.35 \\\hline
# December & 20,87 & 28.57 \\
