library(R.matlab)
library(ggplot2)
setwd('/media/marcelo/OS/Cps/')

df_average <- read.csv('df_cp_average.csv')

tpu_data <- dir(pattern = '.mat')

first = TRUE
for (file in tpu_data){
  print(file)
  opened_file = readMat(file)
  df_location = opened_file$Location.of.measured.points
  df_cp = opened_file$Wind.pressure.coefficients
  mean_cp = apply(df_cp, 2, mean)
  bldg_type = ifelse(substr(file,1,2)=="Cp","lowrise","highrise")
  height = opened_file$Building.height
  
  if(first){
    df = data.frame(
      "file"=rep(file,length(mean_cp)),
      "height"=rep(height,length(mean_cp)),
      "bldg_type"=rep(bldg_type,length(mean_cp)),
      "ratio"=rep(opened_file$Building.breadth/opened_file$Building.depth,length(mean_cp)),
      "Point"=seq(length(mean_cp)),
      "facade"=df_location[4,],
      "angle"=opened_file$Wind.direction.angle,
      "Cp"=mean_cp)
    
    first = FALSE
  }else{
    df_i = data.frame(
      "file"=rep(file,length(mean_cp)),
      "height"=rep(height,length(mean_cp)),
      "bldg_type"=rep(bldg_type,length(mean_cp)),
      "ratio"=rep(opened_file$Building.breadth/opened_file$Building.depth,length(mean_cp)),
      "Point"=seq(length(mean_cp)),
      "facade"=df_location[4,],
      "angle"=opened_file$Wind.direction.angle,
      "Cp"=mean_cp)
    
    df = rbind(df,df_i)
  }
}

df = subset(df, df$facade != 5 & (df$angle == 0 | df$angle == 30 | df$angle == 60 | df$angle == 90 | 
                                    df$angle == 120 | df$angle == 150 | df$angle == 180 | df$angle == 210 | 
                                    df$angle == 240 | df$angle == 270 | df$angle == 300 | df$angle == 330))

df$ratio = as.numeric(as.character(df$ratio))
df_average$ratio = as.numeric(as.character(df_average$ratio))
df$cp_average = NA
df$bldg_type = as.character(df$bldg_type)
for(row in 1:nrow(df)){
  average_cp = subset(
    df_average,
    df_average$bldg_type == df$bldg_type[row] &
    df_average$ratio == df$ratio[row] &
    df_average$facade == df$facade[row] &
    df_average$angle == df$angle[row]
  )
  df$cp_average[row] = average_cp$Cp 
}

df$cp_diff = df$Cp - df$cp_average

hist(df$Cp)
hist(df$cp_average)
hist(df$cp_diff)

ratio = unique(df$ratio)
facade = unique(df$facade)
files = unique(df$file)

bldg_type = unique(df$bldg_type)

maxdiff = 0
ratio_worst = ''
bldg_worst = ''
height_worst = ''

for(bldg in bldg_type){
  ratio = unique(df$ratio[df$bldg_type == bldg])
for(r in ratio){
  height = unique(df$height[df$bldg_type == bldg & df$ratio == r])
  for(h in height){
    dfplot = subset(df, df$bldg_type == bldg & df$ratio == r & df$height == h) 

    diferenca = mean(dfplot$cp_diff**2)**(1/2)
    # print(diferenca)
    if(diferenca > maxdiff){
      ratio_worst = r
      bldg_worst = bldg
      height_worst = h
      maxdiff = diferenca
      print(maxdiff)
    }
  }
}
}

dfplot = subset(df, df$height == .2 & df$ratio == 2)

print(ggplot(dfplot,aes(dfplot$cp_diff)) + geom_histogram(binwidth = .01))
