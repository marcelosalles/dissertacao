library(ggplot2)
#
save_img = function(name,fact=1){
  width = 145* fact
  height = 90 * fact
  file_name = paste('~/dissertacao/latex/img/',name,'.png', sep='')
  ggsave(file_name, width = width, height = height,units = 'mm')
}
# ANN----
#
# basedir = '/media/marcelo/OS/dissertacao/'
basedir = '/home/marcelo/dissertacao/'

sample = read.csv(paste(basedir,'sample_ann.csv',sep=''))
outputs = read.csv(paste(basedir,'ann/means_ann_1.csv',sep=''))
data = cbind(sample,outputs)
write.csv(data, '/home/marcelo/dissertacao/dataset_08-12.csv', row.names = FALSE)

sample_validation = read.csv('/media/marcelo/OS/dissertacao/sample_ann_validation.csv')
outputs_validation = read.csv('/media/marcelo/OS/dissertacao/ann_validation/means_ann_validation.csv')  # ann_validation/means_ann_validation.csv')
data_validation = cbind(sample_validation,outputs_validation)
write.csv(data_validation, '/home/marcelo/dissertacao/dataset_validation_08-12.csv', row.names = FALSE)

sample_test = read.csv('/media/marcelo/OS/dissertacao/sample_ann_test.csv')
outputs_test = read.csv('/media/marcelo/OS/dissertacao/ann_test/means_ann_test.csv')
data_test = cbind(sample_test,outputs_test)
write.csv(data_test, '/home/marcelo/dissertacao/dataset_test_08-10.csv', row.names = FALSE)

df_ann = read.csv('/home/marcelo/dissertacao/dataset_08-06.csv')

# df =read.csv('~/dissertacao/dataset_test_08-10.csv')
# df =read.csv('~/dissertacao/dataset_validation_08-06.csv')
# df =read.csv('~/dissertacao/dataset_08-06.csv')

#
# SOBOL----
sample = read.csv('/media/marcelo/OS/dissertacao/sample_sobol2.csv')
outputs = read.csv('/media/marcelo/OS/dissertacao/sobol2/means_sobol2.csv')

data_set_sobol = cbind(sample,outputs)
write.csv(data_set_sobol,'dataset_sobol.csv', row.names = FALSE)

# EHF ---

parametros = c('Área','Razão L:C sala','Pé-direito','Azimute', 'Altura do pavimento',
               'Absortância','Transmitância', 'Capacidade térmica','PAF',
               'FS do vidro','Sombreamento', 'Ocupação','Fator de abertura','Cobertura exposta',
               'Contato com solo','Razão L:C edifício', 'Velocidade do ar', 'Exposição paredes e janelas')

ehf_s1 = read.csv('/media/marcelo/OS/dissertacao/sobol2/s1_ehf.csv')
ehf_s2 = read.csv('/media/marcelo/OS/dissertacao/sobol2/s2_ehf.csv')

ehf_s1$Parameter
# area         ratio        zone_height  azimuth      floor_height
# absorptance  wall_u       wall_ct      wwr          glass       
# shading      people       open_fac     roof         ground      
# bldg_ratio   v_ar         room_type  
ehf_s1$Parameter = parametros

ehf_s1$Parameter <- factor(ehf_s1$Parameter, levels = ehf_s1$Parameter[order(ehf_s1$ST, decreasing = TRUE)])
# ehf_s1 = ehf_s1[order(ehf_s1$S1,decreasing = TRUE),]
# ehf_s2 = ehf_s2[order(ehf_s2$S2,decreasing = TRUE),]

azimuth = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'azimuth'],ehf_s2$S2[ehf_s2$Parameter_2 == ' azimuth'])
sum(azimuth)
open_fac = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'open_fac'],ehf_s2$S2[ehf_s2$Parameter_2 == ' open_fac'])
sum(open_fac)
v_ar = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'v_ar'],ehf_s2$S2[ehf_s2$Parameter_2 == ' v_ar'])
sum(v_ar)
ground = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'ground'],ehf_s2$S2[ehf_s2$Parameter_2 == ' ground'])
sum(ground)
roof = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'roof'],ehf_s2$S2[ehf_s2$Parameter_2 == ' roof'])
sum(roof)
room_type = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'room_type'],ehf_s2$S2[ehf_s2$Parameter_2 == ' room_type'])
sum(room_type)
wwr_ehf = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'wwr'],ehf_s2$S2[ehf_s2$Parameter_2 == ' wwr'])
sum(wwr_ehf)
area_ehf = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'area']) #,ehf_s2$S2[ehf_s2$Parameter_2 == ' area'])
sum(area_ehf)
people_ehf = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'people'],ehf_s2$S2[ehf_s2$Parameter_2 == ' people'])
sum(people_ehf)
ratio_ehf = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'ratio'],ehf_s2$S2[ehf_s2$Parameter_2 == ' ratio'])
sum(ratio_ehf)
zone_height_ehf = c(ehf_s2$S2[ehf_s2$Parameter_1 == 'zone_height'],ehf_s2$S2[ehf_s2$Parameter_2 == ' zone_height'])
sum(zone_height_ehf)
# TEMP ---

temp_s1 = read.csv('/media/marcelo/OS/dissertacao/sobol2/s1_temp.csv')
temp_s2 = read.csv('/media/marcelo/OS/dissertacao/sobol2/s2_temp.csv')
temp_s1$Parameter = parametros
temp_s1$Parameter <- factor(temp_s1$Parameter, levels = temp_s1$Parameter[order(temp_s1$ST, decreasing = TRUE)])

# temp_s1 = temp_s1[order(temp_s1$S1,decreasing = TRUE),]

azimuth_temp = c(temp_s2$S2[temp_s2$Parameter_1 == 'azimuth'],temp_s2$S2[temp_s2$Parameter_2 == ' azimuth'])
sum(azimuth_temp)
open_fac_temp = c(temp_s2$S2[temp_s2$Parameter_1 == 'open_fac'],temp_s2$S2[temp_s2$Parameter_2 == ' open_fac'])
sum(open_fac_temp)
v_ar_temp = c(temp_s2$S2[temp_s2$Parameter_1 == 'v_ar'],temp_s2$S2[temp_s2$Parameter_2 == ' v_ar'])
sum(v_ar_temp)
ground_temp = c(temp_s2$S2[temp_s2$Parameter_1 == 'ground'],temp_s2$S2[temp_s2$Parameter_2 == ' ground'])
sum(ground_temp)
roof_temp = c(temp_s2$S2[temp_s2$Parameter_1 == 'roof'],temp_s2$S2[temp_s2$Parameter_2 == ' roof'])
sum(roof_temp)
room_type_temp = c(temp_s2$S2[temp_s2$Parameter_1 == 'room_type'],temp_s2$S2[temp_s2$Parameter_2 == ' room_type'])
sum(room_type_temp)
wwr_temp = c(temp_s2$S2[temp_s2$Parameter_1 == 'wwr'],temp_s2$S2[temp_s2$Parameter_2 == ' wwr'])
sum(wwr_temp)

# ach ---

ach_s1 = read.csv('/media/marcelo/OS/dissertacao/sobol2/s1_ach.csv')
ach_s2 = read.csv('/media/marcelo/OS/dissertacao/sobol2/s2_ach.csv')
ach_s1$Parameter = parametros
ach_s1$Parameter <- factor(ach_s1$Parameter, levels = ach_s1$Parameter[order(ach_s1$ST, decreasing = TRUE)])

# ach_s1 = ach_s1[order(ach_s1$S1,decreasing = TRUE),]

azimuth_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'azimuth'],ach_s2$S2[ach_s2$Parameter_2 == ' azimuth'])
sum(azimuth_ach)
open_fac_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'open_fac'],ach_s2$S2[ach_s2$Parameter_2 == ' open_fac'])
sum(open_fac_ach)
v_ar_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'v_ar'],ach_s2$S2[ach_s2$Parameter_2 == ' v_ar'])
sum(v_ar_ach)
ground_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'ground'],ach_s2$S2[ach_s2$Parameter_2 == ' ground'])
sum(ground_ach)
roof_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'roof'],ach_s2$S2[ach_s2$Parameter_2 == ' roof'])
sum(roof_ach)
room_type_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'room_type'],ach_s2$S2[ach_s2$Parameter_2 == ' room_type'])
sum(room_type_ach)
wwr_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'wwr'],ach_s2$S2[ach_s2$Parameter_2 == ' wwr'])
sum(wwr_ach)
area_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'area']) #,ach_s2$S2[ach_s2$Parameter_2 == ' area'])
sum(area_ach)
floor_height_ach = c(ach_s2$S2[ach_s2$Parameter_1 == 'floor_height'],ach_s2$S2[ach_s2$Parameter_2 == ' floor_height'])
sum(floor_height_ach)

# PLOTS ----
cols = c('Efeitos totais' = 'darkblue','1ª ordem' = 'lightblue')
legend_limits = c(0.8, 0.6)
y_limits = c(0,0.4)

ggplot(ehf_s1,aes(ehf_s1$Parameter,ehf_s1$ST)) +
  geom_col(aes(fill='Efeitos totais'))+#'darkblue') +
  geom_col(aes(ehf_s1$Parameter,ehf_s1$S1, fill='1ª ordem'))+#'lightblue') +
  theme(axis.text.x = element_text(angle = 90),legend.position = legend_limits) +
  scale_fill_manual(name=NULL, values=cols)+
  # ggtitle('Análise de Sensibilidade - EHF') +
  xlab('Parâmetro') +
  ylab('Índice de sensibilidade') +
  ylim(y_limits)
save_img('as_ehf')

ggplot(temp_s1,aes(temp_s1$Parameter,temp_s1$ST)) +
  geom_col(aes(fill='Efeitos totais'))+#'darkblue') +
  geom_col(aes(temp_s1$Parameter,temp_s1$S1, fill='1ª ordem'))+#'lightblue') +
  theme(axis.text.x = element_text(angle = 90),legend.position = legend_limits) +
  scale_fill_manual(name=NULL, values=cols)+
  # ggtitle('Análise de Sensibilidade - Temp. Op.') +
  xlab('Parâmetro') +
  ylab('Índice de sensibilidade') +
  ylim(y_limits)
save_img('as_temp')

ggplot(ach_s1,aes(ach_s1$Parameter,ach_s1$ST)) +
  geom_col(aes(fill='Efeitos totais'))+#'darkblue') +
  geom_col(aes(ach_s1$Parameter,ach_s1$S1, fill='1ª ordem'))+#'lightblue') +
  theme(axis.text.x = element_text(angle = 90),legend.position = legend_limits) +
  scale_fill_manual(name=NULL, values=cols)+
  # ggtitle('Análise de Sensibilidade - ACH') +
  xlab('Parâmetro') +
  ylab('Índice de sensibilidade')# +
  # ylim(y_limits)
save_img('as_ach')

factor(ehf_s1$Parameter)
table = table(factor(ehf_s1$Parameter, levels = ehf_s1$Parameter[order(ehf_s1$ST, decreasing = TRUE)]),
              factor(ehf_s1$Parameter, levels = ehf_s1$Parameter[order(ehf_s1$ST, decreasing = TRUE)]))


table = table(factor(ach_s1$Parameter, levels = ach_s1$Parameter[order(ach_s1$ST, decreasing = TRUE)]),
              factor(ach_s1$Parameter, levels = ach_s1$Parameter[order(ach_s1$ST, decreasing = TRUE)]))

table['v_ar','room_type']
table['area','ratio']
typeof(ach_s2$S2[ach_s2$Parameter_1 == 'area' & ach_s2$Parameter_2 == ' v_ar'])

parameters = unique(ach_s2$Parameter_1)
for(param1 in parameters){
  if(length(parameters) > 2){
    parameters = parameters[2:length(parameters)]
    for(param2 in parameters){
      # value = ach_s2$S2[ach_s2$Parameter_1 == param1 & ach_s2$Parameter_2 == param2]
      # param2 = substr(param2,2,nchar(param2))
      # if(param1!=param2){
      #   table[param1,param2] = value
      # }
      print(paste(param1,param2))
    }
  }else{
    print(paste(parameters[2],parameters[3]))
  }
}
# generate 1,000 random numbers from Normal(0,1) distribution
data =  matrix(c(ach_s2$S2,ach_s2$S2,rep(NA,18)), nc=18)
colnames(data) = unique(c(as.character(ach_s2$Parameter_1),substr(ach_s2$Parameter_2,2,nchar(as.character(ach_s2$Parameter_2)))))

# compute Pearson correlation of data and format it nicely
temp = compute.cor(data, 'pearson')
temp[] = plota.format(100 * temp, 0, '', '%')

# plot temp with colorbar, display Correlation in (top, left) cell
plot.table(data,, highlight = TRUE, colorbar = TRUE)

library(corrplot)
cor_matrix_1 = cor(df_ref_cor[,c("temp","temp_max","ach","ehf","area",
                                 "ratio","zone_height", "azimuth","absorptance", 
                                 "wwr","people",'open_fac', 'zn')])

corrplot.mixed(cor_matrix_1, lower = "number", upper = "ellipse",
               tl.pos = "lt", number.cex = 0.6, bg = "black",
               tl.col = "black", tl.srt = 90, tl.cex = 0.8)

# PLOTS ANN ----

# sim_pred <- read.csv('/home/marcelo/Downloads/validation_results_08-05.csv')
sim_pred <- read.csv('/home/marcelo/Downloads/plot_test_08-12.csv')
ggplot(sim_pred,aes(sim_pred$pred,sim_pred$simulado)) +
  geom_point(alpha=.1, col='blue4') +
  geom_abline(col='black') +
  xlab('Predicted EHF') + 
  ylab('Simulated EHF') +
  ylim(c(0,1)) +
  xlim(c(0,1)) +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(mean(abs(sim_pred$pred-sim_pred$simulado)),4))) +
  annotate("text", x = .2, y = .83, label = paste("AE95 =",round(quantile((sim_pred$pred-sim_pred$simulado),.95),4)))
save_img('ann_validation')

# sim_pred_test <- read.csv('/home/marcelo/Downloads/test_results_08-05.csv')
# sim_pred_test <- read.csv('/home/marcelo/Downloads/plot_test_08-06.csv')
sim_pred_test <- read.csv('/home/marcelo/Downloads/plot_test_08-12_ok.csv')
ggplot(sim_pred_test,aes(sim_pred_test$pred,sim_pred_test$simulado)) +
  geom_point(alpha=.15, col='blue4') +
  geom_abline(col='black') +
  xlab('Predicted EHF') + 
  ylab('Simulated EHF') +
  ylim(c(0,1)) +
  xlim(c(0,1)) +
  annotate("text", x = .2, y = .9, label = paste("Média =",round(mean(abs(sim_pred_test$pred-sim_pred_test$simulado)),4))) +
  annotate("text", x = .2, y = .83, label = paste("AE95 =",round(quantile((sim_pred_test$pred-sim_pred_test$simulado),.95),4)))
save_img('ann_test')
