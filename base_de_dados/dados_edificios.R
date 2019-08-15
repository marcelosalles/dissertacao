library(ggplot2)

setwd('~/dissertacao/base_de_dados/')
# ----
df50 <- read.csv('50_edificios.csv')

# for(col in 1:ncol(df50)){
#   for(i in 2:nrow(df50)){
#     if(is.na(df50[i,col]) | df50[i,col] == ""){
#       df50[i,col] = df50[i-1,col]
#     }
#   }
# }

df50$Pé.direito..piso.forro...m. = as.numeric(gsub(',','.',df50$Pé.direito..piso.forro...m.))

df50$Dimensões.total.da.esquadria..LxAxP...m. = as.character(df50$Dimensões.total.da.esquadria..LxAxP...m.)
df50$Dimensões.total.da.esquadria..LxAxP...m.[df50$Dimensões.total.da.esquadria..LxAxP...m. == ''] = NA
df50$Dimensões.total.da.esquadria..LxAxP...m. = gsub(',','.',df50$Dimensões.total.da.esquadria..LxAxP...m.)
df50$Percentual.de.caixilho.operável.... = as.numeric(substr(df50$Percentual.de.caixilho.operável....,1,4))/100

df150 <- read.csv('150_edificios.csv')

df150$Shape[135] = df150$Ratio.between.width.and.length[135] = NA
df150$Ratio.between.width.and.length = as.numeric(as.character(df150$Ratio.between.width.and.length))

office_areas = c(as.numeric(as.character(df150$Office.unit.area..m..)), 37, 74, 148, 32.5, 37)
absorptances = as.numeric(substr(df150$Exterior.wall.absorptance,1,3))

save_hist = function(name,fact=1){
  width = 97* fact
  height = 60 * fact
  file_name = paste('~/dissertacao/latex/img/hist_',name,'.png', sep='')
  ggsave(file_name, width = width, height = height,units = 'mm')
}
FACT = .7

# azimute 
ggplot(df150,aes(df150$Azimuth.angle.of.long.axis.of.building)) +
  geom_histogram(binwidth = 30, boundary=0) +
  ylab('Contagem') +
  xlab('Azimute (°)') +
  scale_x_continuous(breaks = seq(0,180, by=30)) +
save_hist('azimute', fact=FACT)

# formato 
df150$formato = as.character(df150$Shape)
df150$formato[df150$formato != 'L' & df150$formato != 'Rectangular' & df150$formato != 'T'] = "Outros"
df150$formato[is.na(df150$formato)] = "Outros"
df150$formato[df150$formato == 'Rectangular'] = 'Retangular'

df150 <- within(df150, 
                formato <- factor(formato,
                                  levels=names(sort(table(formato),
                                                    decreasing=TRUE))))

ggplot(df150,aes(df150$formato)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Formato do edifício')
save_hist('formato', fact=FACT)

# ratio edificio

ggplot(df150,aes(df150$Ratio.between.width.and.length)) +
  geom_histogram(binwidth = .1, boundary=0) +
  ylab('Contagem') +
  xlab('Razão entre menor e maior\ndimensão do edifício (-)') +
  scale_x_continuous(limits=c(0,1), breaks = seq(0,1, by=.2)) 
save_hist('ratio_edificio', fact=FACT)

# area edificio

ggplot(df150,aes(df150$Total.floor.area..m..)) +
  geom_histogram(binwidth = 10, boundary=0) +
  ylab('Contagem') +
  xlab('Área do pavimento (m²)') +
  xlim(c(0,max(df150$Total.floor.area..m..)))
save_hist('area_edificio', fact=FACT)

# numero de pavimentos

ggplot(df150,aes(df150$Number.of.floors)) +
  geom_histogram(binwidth = 1, boundary=0) +
  ylab('Contagem') +
  xlab('Número de pavimentos') +
  xlim(c(0,max(df150$Number.of.floors)))
save_hist('numero_pavimentos', fact=FACT)

# absortancia
df_abs = data.frame('abs' = absorptances)

ggplot(df_abs,aes(df_abs$abs)) +
  geom_histogram(binwidth = .1, boundary=0) +
  ylab('Contagem') +
  xlab('Absortância da parede externa (-)') +
  scale_x_continuous(limits = c(0,1),breaks = seq(0,1, by=.2)) 

save_hist('absortancia', fact=FACT)

# cor cobertura
df150$cobcolor = as.character(df150$Roof.color)
df150$cobcolor[df150$cobcolor != 'Gray' & 
                 df150$cobcolor != 'White' & 
                 df150$cobcolor != 'Gray/ White' &
                 df150$cobcolor != 'Beige'] = "Outros"
df150$cobcolor[is.na(df150$cobcolor)] = "Outros"
df150$cobcolor[df150$cobcolor == 'Gray'] = 'Cinza'
df150$cobcolor[df150$cobcolor == 'White'] = 'Branco'
df150$cobcolor[df150$cobcolor == 'Gray/ White'] = 'Cinza/\nBranco'  # 'Cinza / Branco'
df150$cobcolor[df150$cobcolor == 'Beige'] = 'Bege'

df150 <- within(df150, 
                cobcolor <- factor(cobcolor, 
                                  levels=c('Cinza','Branco','Cinza/\nBranco','Bege',"Outros")))  # ,'Cinza / Branco'

ggplot(df150,aes(df150$cobcolor)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Cor da cobertura') #+
  theme(axis.text.x = element_text(angle = 45))
save_hist('cor_cobertura', fact=FACT)

# tipo de vidro
df150$tipo_vidro = as.character(df150$Glazing.type)
df150$tipo_vidro[df150$tipo_vidro == 'Clear glass'] = 'Vidro incolor'
df150$tipo_vidro[df150$tipo_vidro == 'Laminated glass'] = 'Vidro laminado' 

ggplot(df150,aes(df150$tipo_vidro)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Tipo de vidro')
save_hist('tipo_vidro', fact=FACT)

# sombreamento
df150$sombreamento = as.character(df150$Exterior.solar.shading.devices)
df150$sombreamento[!grepl('No',df150$sombreamento) &
                     !grepl('Balc',df150$sombreamento)] = 'Outros'
df150$sombreamento = as.character(df150$sombreamento)
df150$sombreamento[grepl('Balc',df150$sombreamento)] = 'Sacada'
df150$sombreamento[grepl('No',df150$sombreamento)] = 'Inexistente'

df150 <- within(df150, 
                sombreamento <- factor(sombreamento, 
                                  levels=names(sort(table(sombreamento), 
                                                    decreasing=TRUE))))

ggplot(df150,aes(df150$sombreamento)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Sombreamento')
save_hist('sombreamento', fact=FACT)

# tipo de esquadria
df150$tipo_esquadria = as.character(df150$Window.frame.type)
df150$tipo_esquadria[df150$tipo_esquadria != 'Top hung'] = 'Outros'
df150$tipo_esquadria[df150$tipo_esquadria == 'Top hung'] = 'Maxim-Ar'
# df150$tipo_esquadria[df150$tipo_esquadria == 'Sliding'] = 'Correr'
# df150$tipo_esquadria[df150$tipo_esquadria == 'Top hung\nSliding (Balcony)'] = 'Maxim-Ar\nCorrer (Sacada)'
# df150$tipo_esquadria[df150$tipo_esquadria == 'Sliding/ Top hung'] = 'Correr/Maxim-Ar'
# df150$tipo_esquadria[df150$tipo_esquadria == 'Top Pivoted'] = 'Pivotante'
# df150 <- within(df150,
#                 Window.frame.type <- factor(Window.frame.type,
#                                             levels=names(sort(table(Window.frame.type),
#                                                               decreasing=TRUE))))

ggplot(df150,aes(df150$tipo_esquadria)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Tipo de esquadria')
save_hist('esquadria', fact=FACT)

# areas zonas
df_area = data.frame('area' = office_areas[!is.na(office_areas)])

ggplot(df_area,aes(df_area$area)) +
  geom_histogram(binwidth = 5, boundary=0) +
  ylab('Contagem') +
  xlab('Áreas da sala (m²)') +
  scale_x_continuous(limits=c(0,max(df_area$area)), breaks = seq(0,160, by=20))
save_hist('area_zonas', fact=FACT)

# SOH OS 50!!!

# espessura da parede

ggplot(df50,aes(df50$Espessura.da.parede..m.)) +
  geom_histogram(binwidth = .05, boundary=0) +
  ylab('Contagem') +
  xlab('Espessura da parede (m)')
save_hist('espessura_parede', fact=FACT)

# tipo de VN

df_vn = data.frame('vn' = df50$Estratégia.de.ventilação.natural[which(df50$Estratégia.de.ventilação.natural != '')])
df_vn$vn = as.character(df_vn$vn)
df_vn$vn[grepl('Cruzada',df_vn$vn)] = 'Cruzada'
df_vn$vn[grepl('Unilateral',df_vn$vn)] = 'Unilateral'
df_vn <- within(df_vn,
                vn <- factor(vn,
                             levels=names(sort(table(vn),
                                               decreasing=TRUE))))

ggplot(df_vn,aes(df_vn$vn)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Tipo de ventilação natural')
save_hist('tipo_vn', fact=FACT)

# formato da sala

df_formasala = data.frame('forma' = df50$Formato.da.sala[which(df50$Formato.da.sala != '')])

df_formasala <- within(df_formasala, 
                       forma <- factor(forma, 
                             levels=names(sort(table(forma), 
                                               decreasing=TRUE))))

ggplot(df_formasala,aes(df_formasala$forma)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Formato da sala')
save_hist('formato_sala', fact=FACT)

# ratio da sala

df50$ratio = df50$Dimensões..LxC...m./df50$X

ggplot(df50,aes(df50$ratio)) +
  geom_histogram(binwidth = .1, boundary=0) +
  ylab('Contagem') +
  xlab('Razão entre menor e maior\ndimensão da sala (-)') +
  scale_x_continuous(limits=c(0,1), breaks = seq(0,1, by=.2)) 
save_hist('ratio_sala', fact=FACT)

# pe direito

ggplot(df50,aes(df50$Pé.direito..piso.forro...m.)) +
  geom_histogram(binwidth = .1, boundary=0) +
  ylab('Contagem') +
  xlab('Pé-direito (m)')
save_hist('pe_direito', fact=FACT)

# PAF

ggplot(df50,aes(df50$PAF.total.da.sala..../100)) +
  geom_histogram(binwidth = .1, boundary=0) +
  ylab('Contagem') +
  xlab('Percentual de abertura\nna fachada (-)')
save_hist('PAF', fact=FACT)

# altura da janela

df50$hjan = as.numeric(substr(df50$Dimensões.total.da.esquadria..LxAxP...m., 8,11))

ggplot(df50,aes(df50$hjan)) +
  geom_histogram(binwidth = .1, boundary=0) +
  ylab('Contagem') +
  xlab('Altura da esquadria (m)')
save_hist('hjan', fact=FACT)

# fator de abertura

ggplot(df50,aes(df50$Percentual.de.caixilho.operável....)) +
  geom_histogram(binwidth = .1, boundary=0) +
  ylab('Contagem') +
  xlab('Fator de abertura da janela (-)') +
  scale_x_continuous(limits=c(0,1), breaks = seq(0,1, by=.2)) 
save_hist('openfac', fact=FACT)

#
# ---- resultados ----
min(df150$Number.of.floors)
max(df150$Number.of.floors)
mean(df150$Number.of.floors)
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}
getmode(df150$Number.of.floors)

resume_feat = function(feature){
  feature = feature[!is.na(feature)]
  print(min(feature))
  print(max(feature))
  print(mean(feature))
  print(median(feature))
  print(getmode(feature))
}

resume_feat(office_areas[!is.na(office_areas)])
resume_feat(as.numeric(df50$Pé.direito..piso.forro...m.))
resume_feat(df50$ratio[!is.na(df50$ratio)])
resume_feat(df150$Ratio.between.width.and.length)
resume_feat(absorptances)
resume_feat(df50$PAF.total.da.sala..../100)

varia#
# rest ----
df <- cbind(df50, 'Location'=NA,'Address'=NA,'Telephone'=NA,'Contacts'=NA,'Lease.cost'=NA,'Bldg.Ratio'=NA,'Total.floor.area'=NA,
            'Plenum.height'=NA,'Glazing.type'=NA,'Spandrel.height'=NA,'Control.system'=NA, 'Azimuth.angle'=NA)

df <- data.frame('ID' = df150$Nº, 'Bldg.Name'=df150$Building, 'Year.of.construction' = df150$Year.of.construction, 'Ext.wall.color'=df150$Exterior.wall.color,
                 'Ext.wall.abs'=df150$Exterior.wall.absorptance,'Ext.coating'=NA, 'Roof.color'=df150$Roof.color, 'Ext.wall.width' = df150$Exterior.wall,
                 'n.Floors'=df150$Number.of.floors, 'Floor.Shape'=df150$Shape, 'Solar.orientation'=df150$Solar.orientation..long.axis.,
                 'office.orientation'=NA, 'office.shape'=NA, 'office.width'=NA,'office.depth'=df150$Room.depth..m., 'ceiling.height'=df150$Ceiling.height..m.,
                 'office.area'=df150$Office.unit.area..m.., 'window.orientation'=NA,'west.WWR'=NA,'north.WWR'=NA,'east.WWR'=NA,'south.WWR'=NA,'WWR'=df150$WWR....,
                 'west.n.windows'=NA,'north.n.windows'=NA,'east.n.windows'=NA,'south.n.windows'=NA,'opening.type'=NA,'window.model'=df150$Window.frame.type,
                 'window.dimension'=df150$Window.geometry..length.x.height...m.)
colnames(df50) <- c("ID","Bldg.Name","Year.of.construction","Ext.wall.color","Ext.wall.abs","Ext.coating",
                    "Roof.color","wall.width","n.floors","bldg.Shape","Orientação.solar..eixo.longitudinal.","Posição.longitudinal.da.sala",
                    "Office.shape","bldg.width","bldg.depth","Ceiling.height","Office.unit.area",
                    "Orientação.da.fachada.envidraçada","PAF.por.fachada.da.sala....","PAF.total.da.sala....",
                    "Número.de.esquadrias.na.fachada","Tipo.de.esquadria","Modelo.de.esquadria",
                    "Dimensões.total.da.esquadria..LxAxP...m.","Área.transparente.da.esquadria..m..",
                    "Tipo.de.vidro..transparência.e.coloração.","X.1","Dimensões.da.folha.operável..LxA...m.",
                    "X.2","Número.total.de.folhas","Número.de.folhas.operáveis","Percentual.de.caixilho.operável....",
                    "Área.de.caxilho.operável.de.uma.folha...m..","Área.de.caixilho.operável.total.da.esquadria..m..",
                    "Área.efetiva.de.abertura..m....Abertura.de.segurança.","Área.efetiva.de.abertura..m....Abertura.máxima.",
                    "Altura.do.peitoril","Tipo.de.elemento.de.proteção","Localização..fachada.frontal.ou.lateral.",
                    "Dimensões..LxAxP.","Estratégia.de.ventilação.natural","Tipo.de.ar.condicionado",
                    "Localização.da.unidade.externa.do.ar.condicionado")

df150$Telephone <- NULL
df150$Contacts <- NULL

colnames(df150) <- c('ID','Bldg.Name','Location','Adress',"Telephone","Contacts","Year.of.construction",
                     "Azimuth.angle","Solar.orientation..long.axis.","bldg.Shape",
                     "Ratio.between.width.and.length","Total.floor.area..m..","Office.unit.area",
                     "n.floors","Ext.wall.color","Ext.wall.abs","Roof.color",
                     "Glazing.type","Exterior.solar.shading.devices","Room.depth..m.","Ceiling.height",
                     "Plenum.height..m.","Spandrel.height..m.","Exterior.wall","WWR",
                     "Exterior.solar.shading.devices.dimension","Natural.ventilation.strategy..cross.or.single.sided.",
                     "Window.frame.type","Window.opening.effective.area","Window.geometry..length.x.height...m.",
                     "Start.height.of.opening..m.","Control.system","System.type","Location.1")    
