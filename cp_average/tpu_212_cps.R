library(R.matlab)
setwd('/media/marcelo/OS/Cps/')

# Baixar dados ----

cp00 <- readMat('T212_4_000_1.mat')
cp30 <- readMat('T212_4_030_1.mat')
cp60 <- readMat('T212_4_060_1.mat')
cp90 <- readMat('T212_4_090_1.mat')

df_len = 24 * 8 * 4
df = data.frame('floor'=rep(NA,df_len), 'zone'=rep(NA,df_len), 'angle'=rep(NA,df_len), 'cp'=rep(NA,df_len))

line = 1
for(f in list(cp00,cp30,cp60,cp90)){
  for(i in 0:7){
    print(i)
    #################
    # 0
    df$floor[line] = i
    df$zone[line] = 0
    df$angle[line] = f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+1]),mean(f$Wind.pressure.coefficients[1:32768,i*30+2]),mean(f$Wind.pressure.coefficients[1:32768,i*30+3]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 0
    df$angle[line] = 360-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+8]),mean(f$Wind.pressure.coefficients[1:32768,i*30+9]),mean(f$Wind.pressure.coefficients[1:32768,i*30+10]))
    line = line + 1
    
    # 1
    df$floor[line] = i
    df$zone[line] = 1
    df$angle[line] = f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+4]),mean(f$Wind.pressure.coefficients[1:32768,i*30+5]),mean(f$Wind.pressure.coefficients[1:32768,i*30+6]),mean(f$Wind.pressure.coefficients[1:32768,i*30+7]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 1
    df$angle[line] = 360-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+4]),mean(f$Wind.pressure.coefficients[1:32768,i*30+5]),mean(f$Wind.pressure.coefficients[1:32768,i*30+6]),mean(f$Wind.pressure.coefficients[1:32768,i*30+7]))
    line = line + 1
    
    # 2
    df$floor[line] = i
    df$zone[line] = 2
    df$angle[line] = f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+8]),mean(f$Wind.pressure.coefficients[1:32768,i*30+9]),mean(f$Wind.pressure.coefficients[1:32768,i*30+10]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 2
    df$angle[line] = 360-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+1]),mean(f$Wind.pressure.coefficients[1:32768,i*30+2]),mean(f$Wind.pressure.coefficients[1:32768,i*30+3]))
    line = line + 1
    
    # 3
    df$floor[line] = i
    df$zone[line] = 3
    df$angle[line] = (f[['Wind.direction.angle']]+270)%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+11]),mean(f$Wind.pressure.coefficients[1:32768,i*30+12]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 3
    df$angle[line] = 90-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+14]),mean(f$Wind.pressure.coefficients[1:32768,i*30+15]))
    line = line + 1
    
    # 4
    df$floor[line] = i
    df$zone[line] = 4
    df$angle[line] = (f[['Wind.direction.angle']]+270)%%360
    df$cp[line] = mean(f$Wind.pressure.coefficients[1:32768,i*30+13])
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 4
    df$angle[line] = 90-f[['Wind.direction.angle']]
    df$cp[line] = mean(f$Wind.pressure.coefficients[1:32768,i*30+13])
    line = line + 1
    
    # 5
    df$floor[line] = i
    df$zone[line] = 5
    df$angle[line] = (f[['Wind.direction.angle']]+270)%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+14]),mean(f$Wind.pressure.coefficients[1:32768,i*30+15]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 5
    df$angle[line] = 90-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+11]),mean(f$Wind.pressure.coefficients[1:32768,i*30+12]))
    line = line + 1
    
    ######## outro lado
    
    # 0
    df$floor[line] = i
    df$zone[line] = 0
    df$angle[line] = (f[['Wind.direction.angle']]+180)%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+16]),mean(f$Wind.pressure.coefficients[1:32768,i*30+17]),mean(f$Wind.pressure.coefficients[1:32768,i*30+18]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 0
    df$angle[line] = 180-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+16]),mean(f$Wind.pressure.coefficients[1:32768,i*30+17]),mean(f$Wind.pressure.coefficients[1:32768,i*30+18]))
    line = line + 1
    
    # 1
    df$floor[line] = i
    df$zone[line] = 1
    df$angle[line] = (f[['Wind.direction.angle']]+180)%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+19]),mean(f$Wind.pressure.coefficients[1:32768,i*30+20]),mean(f$Wind.pressure.coefficients[1:32768,i*30+21]),mean(f$Wind.pressure.coefficients[1:32768,i*30+22]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 1
    df$angle[line] = 180-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+19]),mean(f$Wind.pressure.coefficients[1:32768,i*30+20]),mean(f$Wind.pressure.coefficients[1:32768,i*30+21]),mean(f$Wind.pressure.coefficients[1:32768,i*30+22]))
    line = line + 1
    
    # 2
    df$floor[line] = i
    df$zone[line] = 2
    df$angle[line] = (f[['Wind.direction.angle']]+180)%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+23]),mean(f$Wind.pressure.coefficients[1:32768,i*30+24]),mean(f$Wind.pressure.coefficients[1:32768,i*30+25]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 2
    df$angle[line] = 180-f[['Wind.direction.angle']]
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+16]),mean(f$Wind.pressure.coefficients[1:32768,i*30+17]),mean(f$Wind.pressure.coefficients[1:32768,i*30+18]))
    line = line + 1
    
    # 3
    df$floor[line] = i
    df$zone[line] = 3
    df$angle[line] = (f[['Wind.direction.angle']]+90)%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+26]),mean(f$Wind.pressure.coefficients[1:32768,i*30+27]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 3
    df$angle[line] = (270-f[['Wind.direction.angle']])%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+29]),mean(f$Wind.pressure.coefficients[1:32768,i*30+30]))
    line = line + 1
    
    # 4
    df$floor[line] = i
    df$zone[line] = 4
    df$angle[line] = (f[['Wind.direction.angle']]+90)%%360
    df$cp[line] = mean(f$Wind.pressure.coefficients[1:32768,i*30+28])
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 4
    df$angle[line] = (270-f[['Wind.direction.angle']])%%360
    df$cp[line] = mean(f$Wind.pressure.coefficients[1:32768,i*30+28])
    line = line + 1
    
    # 5
    df$floor[line] = i
    df$zone[line] = 5
    df$angle[line] = (f[['Wind.direction.angle']]+90)%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+29]),mean(f$Wind.pressure.coefficients[1:32768,i*30+30]))
    line = line + 1
    
    df$floor[line] = i
    df$zone[line] = 5
    df$angle[line] = (270-f[['Wind.direction.angle']])%%360
    df$cp[line] = mean(mean(f$Wind.pressure.coefficients[1:32768,i*30+26]),mean(f$Wind.pressure.coefficients[1:32768,i*30+27]))
    line = line + 1
    
  }
}

df = subset(df, df$angle != 360)
length(unique(df$floor))*length(unique(df$zone))*length(unique(df$angle))
df_copy = df
df_len = 24 * 8 * 4
df2 = data.frame('floor'=rep(NA,df_len), 'zone'=rep(NA,df_len), 'angle'=rep(NA,df_len), 'cp'=rep(NA,df_len))

line = 1
for(f in unique(df$floor)){
  for(z in unique(df$zone)){
    for(a in unique(df$angle)){
      subdf = subset(df, df$floor == f & df$zone == z & df$angle == a)
      if(nrow(subdf) > 1){
        
        df2$floor[line] = f
        df2$zone[line] = z
        df2$angle[line] = a
        df2$cp[line] = mean(subdf$cp)
        line = line + 1
        
        df = subset(df, !(df$floor == f & df$zone == z & df$angle == a))
      }
    }
  }
}

df2 = subset(df2, !is.na(df2$floor))

# df = df_copy

df = rbind(df, df2)

length(unique(df$floor))*length(unique(df$zone))*length(unique(df$angle))

write.csv(df, 'TPU_212_cp.csv', row.names = FALSE)

#####
library(ggplot2)

save_img = function(name,fact=1){
  width = 145* fact
  height = 90 * fact
  file_name = paste('~/dissertacao/latex/img/',name,'.png', sep='')
  ggsave(file_name, width = width, height = height,units = 'mm')
}

# df = rbind(
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster0/means_cluster0.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster1/means_cluster1.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster2/means_cluster2.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster3/means_cluster3.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster4/means_cluster4.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster5/means_cluster5.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster6/means_cluster6.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster7/means_cluster7.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster8/means_cluster8.csv'),
#   read.csv('/media/marcelo/OS/Cps/TPU/cluster9/means_cluster9.csv')
# )

# df = rbind(
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster0/means_cluster0.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster1/means_cluster1.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster2/means_cluster2.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster3/means_cluster3.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster4/means_cluster4.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster5/means_cluster5.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster6/means_cluster6.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster7/means_cluster7.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster8/means_cluster8.csv'),
#   read.csv('/media/marcelo/OS/dissertacao/cp_average/cluster9/means_cluster9.csv')
# )

df = read.csv('/home/marcelo/dissertacao/cp_average/means.csv')

df_tpu = subset(df, substr(df$file,7,7) == 't')
df_ave = subset(df, substr(df$file,7,7) == 'a')
df_dif = data.frame(
  'case' = substr(df_tpu$file,5,8),
  'zone' = df_tpu$zone,
  'temp' = df_ave$temp - df_tpu$temp,
  'ach' = df_ave$ach - df_tpu$ach,
  'ehf' = df_ave$ehf - df_tpu$ehf
)

ach_mean = mean(df_dif$ach)
ehf_mean = mean(df_dif$ehf)
temp_mean = mean(df_dif$temp)

ggplot(df_dif,aes(df_dif$ehf)) +
  geom_histogram(binwidth = .001)+
  ggtitle('Diferenças no EHF') +
  xlab('EHF analítico - EHF tpu') +
  ylab('Número de casos') +
  annotate("text", x = -.03, y = 200, label = paste("Média =",round(ehf_mean,4))) +
  annotate("text", x = -.03, y = 200*.9, label = paste("AE95 =",round(quantile(abs(df_dif$ehf),.95),4)))
save_img('cpaverage_EHF')

ggplot(df_dif,aes(df_dif$ach)) +
  geom_histogram(binwidth = .5) +
  ggtitle('Diferenças no ACH') +
  xlab('ACH analítico - ACH tpu (ACH)') +
  ylab('Número de casos') +
  annotate("text", x = -12, y = 700, label = paste("Média =",round(ach_mean,3),'ach'))
save_img('cpaverage_ACH')

ggplot(df_dif,aes(df_dif$temp)) +
  geom_histogram(binwidth = .1)+
  ggtitle('Diferenças na Temperatura Operativa') +
  xlab('Temperatura analítico - Temperatura tpu (°C)') +
  ylab('Número de casos') +
  annotate("text", x = -.45, y = 800, label = paste("Média =",round(temp_mean,4))) +
  annotate("text", x = -.45, y = 800*.9, label = paste("AE95 =",round(quantile(abs(df_dif$temp),.95),4))) 
save_img('cpaverage_temp')

# SCAATTERPLOT

ggplot(df_tpu,aes(df_tpu$ehf,df_ave$ehf)) +
  geom_point(alpha=.25)+
  geom_abline() +
  ggtitle('Comparação do EHF') +
  xlab('TPU') +
  ylab('Analítico') +
  annotate("text", x = .25, y = .9, label = paste("Média =",round(ehf_mean,4))) +
  annotate("text", x = .25, y = .8, label = paste("AE95 =",round(quantile(abs(df_dif$ehf),.95),4)))
save_img('cpaverage_EHF_scatter')

ggplot(df_tpu,aes(df_tpu$ach,df_ave$ach)) +
  geom_point(alpha=.25)+
  geom_abline() +
  ggtitle('Comparação do ACH') +
  xlab('TPU') +
  ylab('Analítico') +
  annotate("text", x = 10, y = 90, label = paste("Média =",round(ach_mean,4))) +
  annotate("text", x = 10, y = 80, label = paste("AE95 =",round(quantile(abs(df_dif$ach),.95),2)))
save_img('cpaverage_ACH_scatter')

ggplot(df_tpu,aes(df_tpu$temp,df_ave$temp)) +
  geom_point(alpha=.25)+
  geom_abline() +
  ggtitle('Comparação da Temp. Operativa') +
  xlab('TPU') +
  ylab('Analítico') +
  annotate("text", x = 24, y = 33, label = paste("Média =",round(temp_mean,2))) +
  annotate("text", x = 24, y = 32, label = paste("AE95 =",round(quantile(abs(df_dif$temp),.95),2)))
save_img('cpaverage_temp_scatter')

ggplot(df_tpu,aes(df_tpu$ehf)) +
  geom_histogram(binwidth = .05)

sample = read.csv('/media/marcelo/OS/dissertacao/sample_cp_average.csv')
