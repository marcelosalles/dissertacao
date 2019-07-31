library(ggplot2)

setwd('~/dissertacao/base_de_dados/')

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

# azimute 
ggplot(df150,aes(df150$Azimuth.angle.of.long.axis.of.building)) +
  geom_histogram(binwidth = 30) +
  ylab('Contagem') +
  xlab('Azimute (°)')
save_hist('azimute')

# formato 
df150$formato = as.character(df150$Shape)
df150$formato[df150$formato != 'L' & df150$formato != 'Rectangular' & df150$formato != 'T'] = "Outros"
df150$formato[is.na(df150$formato)] = "Outros"

df150 <- within(df150, 
                formato <- factor(formato,
                                  levels=names(sort(table(formato),
                                                    decreasing=TRUE))))

ggplot(df150,aes(df150$formato)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Formato do edifício')
save_hist('formato')

# ratio edificio

ggplot(df150,aes(df150$Ratio.between.width.and.length)) +
  geom_histogram(binwidth = .1) +
  ylab('Contagem') +
  xlab('Razão entre dimensões do edifício')
save_hist('ratio_edificio')

# area edificio

ggplot(df150,aes(df150$Total.floor.area..m..)) +
  geom_histogram(binwidth = 10) +
  ylab('Contagem') +
  xlab('Área do pavimento')
save_hist('area_edificio')

# numero de pavimentos

ggplot(df150,aes(df150$Number.of.floors)) +
  geom_histogram(binwidth = 1) +
  ylab('Contagem') +
  xlab('Número de pavimentos')
save_hist('numero_pavimentos')

# absortancia
df_abs = data.frame('abs' = absorptances)

ggplot(df_abs,aes(df_abs$abs)) +
  geom_histogram(binwidth = .1) +
  ylab('Contagem') +
  xlab('Absortância da parede externa')
save_hist('absortancia')

# cor cobertura
df150$cobcolor = as.character(df150$Roof.color)
df150$cobcolor[df150$cobcolor != 'Gray' & 
                 df150$cobcolor != 'White' & 
                 df150$cobcolor != 'Gray/ White' &
                 df150$cobcolor != 'Beige'] = "Outros"
df150$cobcolor[is.na(df150$cobcolor)] = "Outros"

df150 <- within(df150, 
                cobcolor <- factor(cobcolor, 
                                  levels=c('Gray','White','Gray/ White','Beige',"Outros")))

ggplot(df150,aes(df150$cobcolor)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Cor da cobertura')
save_hist('cor_cobertura')

# tipo de vidro

ggplot(df150,aes(df150$Glazing.type)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Tipo de vidro')
save_hist('tipo_vidro')

# sombreamento
unique(df150$Exterior.solar.shading.devices)
df150$Exterior.solar.shading.devices = as.character(df150$Exterior.solar.shading.devices)
df150$Exterior.solar.shading.devices[grepl('Balc',df150$Exterior.solar.shading.devices)] = 'Varanda'

df150 <- within(df150, 
                Exterior.solar.shading.devices <- factor(Exterior.solar.shading.devices, 
                                  levels=names(sort(table(Exterior.solar.shading.devices), 
                                                    decreasing=TRUE))))

ggplot(df150,aes(df150$Exterior.solar.shading.devices)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Sombreamento')
save_hist('sombreamento')

# tipo de esquadria
df150 <- within(df150,
                Window.frame.type <- factor(Window.frame.type,
                                            levels=names(sort(table(Window.frame.type),
                                                              decreasing=TRUE))))

ggplot(df150,aes(df150$Window.frame.type)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Tipo de esquadria')
save_hist('esquadria')

# areas zonas
df_area = data.frame('area' = office_areas)

ggplot(df_area,aes(df_area$area)) +
  geom_histogram(binwidth = 5) +
  ylab('Contagem') +
  xlab('Áreas do escritórios (m²)')
save_hist('area_zonas')

# SOH OS 50!!!

# espessura da parede

ggplot(df50,aes(df50$Espessura.da.parede..m.)) +
  geom_histogram(binwidth = .05) +
  ylab('Contagem') +
  xlab('Espessura da parede (m)')
save_hist('espessura_parede')

# tipo de VN

df_vn = data.frame('vn' = df50$Estratégia.de.ventilação.natural[which(df50$Estratégia.de.ventilação.natural != '')])

df_vn <- within(df_vn,
                vn <- factor(vn,
                             levels=names(sort(table(vn),
                                               decreasing=TRUE))))

ggplot(df_vn,aes(df_vn$vn)) +
  geom_bar() +
  ylab('Contagem') +
  xlab('Tipo de ventilação natural')
save_hist('tipo_vn')

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
save_hist('formato_sala')

# ratio da sala

df50$ratio = df50$X/df50$Dimensões..LxC...m.

ggplot(df50,aes(df50$ratio)) +
  geom_histogram(binwidth = .1) +
  ylab('Contagem') +
  xlab('Razão entre as dimensões da sala')
save_hist('ratio_sala')

# pe direito

ggplot(df50,aes(df50$Pé.direito..piso.forro...m.)) +
  geom_histogram(binwidth = .1) +
  ylab('Contagem') +
  xlab('Pé-direito (m)')
save_hist('pe_direito')

# PAF

ggplot(df50,aes(df50$PAF.total.da.sala..../100)) +
  geom_histogram(binwidth = .1) +
  ylab('Contagem') +
  xlab('PAF')
save_hist('PAF')

# altura da janela

df50$hjan = as.numeric(substr(df50$Dimensões.total.da.esquadria..LxAxP...m., 8,11))

ggplot(df50,aes(df50$hjan)) +
  geom_histogram(binwidth = .1) +
  ylab('Contagem') +
  xlab('Altura da esquadria (m)')
save_hist('hjan')

# fator de abertura

ggplot(df50,aes(df50$Percentual.de.caixilho.operável....)) +
  geom_histogram(binwidth = .1) +
  ylab('Contagem') +
  xlab('Fator de abertura da janela')
save_hist('openfac')

#
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
