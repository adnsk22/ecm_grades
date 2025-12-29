setwd("/kuacc/users/adansik22/network_modeling/")

library(ComplexHeatmap)
library(circlize)
library(colorspace)
library(tidyverse)

dirlist=list.files("patients/")

for (i in dirlist){
  
  data_path=paste0("patients/", i, "/", i, "_membership_df.csv")
  attribute_path=paste0("patients/", i, "/", i, "_node_attributes.csv")
  png_path1=paste0("patients/", i, "/", i, "_membership_heatmap.png")
  opt_data=paste0("patients/", i, "/", i, "_opt_data.csv")
  
  #raw data
  data=read_csv(data_path) %>% select("nodes"=...1, everything())

  #membership
  membership=data %>% filter(nodes!="Covering_nodes" & nodes!="Total_nodes" & nodes!="Component_number")

  #node attributes
  node_attributes=read_csv(attribute_path)%>% 
    select("nodes"=...1, everything()) %>% 
    inner_join(membership) %>% 
    select(-starts_with("W")) %>% 
    mutate(log10_degree=log10(degree)) %>% 
    mutate(Category=ifelse(is.na(Category),"INT",Category)) %>% 
    select("category"=Category, everything())
  
  #terminal number
  terminals=node_attributes %>% 
    filter(terminal==TRUE) %>% 
    distinct(nodes) %>% 
    count() %>% 
    as.vector()

  #optimization
  optimization_data=data %>% 
    filter(nodes=="Covering_nodes" | nodes=="Total_nodes" | nodes=="Component_number") %>% 
    column_to_rownames("nodes") %>% 
    t() %>% 
    as.data.frame() %>% 
    mutate(Terminal_coverage=Covering_nodes/terminals$n) %>% 
    mutate(parameters=rownames(.)) %>% 
    separate(parameters, into = c("no1","w","no2","b","no3","g"), sep = "_") %>% 
    select(-starts_with("no")) %>% 
    mutate_all(as.numeric)
  
  #save
  write_csv(optimization_data, opt_data)
  
  membership=membership %>% column_to_rownames("nodes")
  node_attributes=node_attributes %>% column_to_rownames("nodes")
  node_attributes=node_attributes[rownames(membership),c("category","prize", "log10_degree")]

  # Top annotation
  ha = HeatmapAnnotation(df=node_attributes, 
                        col=list(
                          prize = colorRamp2(c(0,max(node_attributes$prize)), c("white", "orange")),
                          log10_degree=colorRamp2(c(0,1.5,max(node_attributes$log10_degree)), c("blue", "white", "red"))),
                        annotation_legend_param=list(
                          prize=list(legend_direction="horizontal"),
                          log10_degree=list(legend_direction="horizontal"))
                        )
  #Heatmap
  ht = Heatmap(
          t(membership), 
          name="membership", 
          col=c("white", "black"), 
          show_column_names=F, 
          show_row_names = T,
          top_annotation=ha,
          column_title = i,
          column_title_side = "bottom",
          row_names_gp = gpar(fontsize = 5)) + 
    Heatmap(optimization_data$w, name="W", col=colorRamp2(c(0, max(optimization_data$w)), c("white", "red")), width=unit(6, "mm")) +
    Heatmap(optimization_data$b, name="B", col=colorRamp2(c(0, max(optimization_data$b)), c("white", "blue")), width=unit(6, "mm")) +
    Heatmap(optimization_data$g, name="G", col=colorRamp2(c(0, max(optimization_data$g)), c("white", "green")), width=unit(6, "mm"))+
    Heatmap(optimization_data$Terminal_coverage, name="coverage", col=colorRamp2(c(0.99,1), c("white","purple")), width=unit(6, "mm"))+
    Heatmap(optimization_data$Total_nodes, name="total", col=colorRamp2(c(mean(optimization_data$Total_nodes),max(optimization_data$Total_nodes)), c("white","pink")), width=unit(6, "mm"))+
    Heatmap(optimization_data$Component_number, name="component",col=colorRamp2(c(1,2),c("yellow","white")), width=unit(6, "mm"))            

  #save
  png(png_path1)
  draw(ht, heatmap_legend_side = "top", annotation_legend_side = "top")
  dev.off()
}

parameter_list = data.frame(w = numeric(), b = numeric(), g = numeric())

for (i in dirlist){
 opt_data=paste0("patients/", i, "/", i, "_opt_data.csv")
 opt=read.csv(opt_data) %>% 
  filter(Component_number==1 & Terminal_coverage==1) %>% 
  filter(w==2 & b==2) %>% # this part may be changed or switched off
  arrange(Total_nodes) %>% 
  top_n(2, wt = -Total_nodes) %>% 
  select(w,b,g)
 rownames(opt)=paste(i, opt$g, sep = "_")
 parameter_list=rbind(parameter_list,opt)
}

g34_parameter_list=parameter_list %>% rownames_to_column("patients")

#save
write_csv(g34_parameter_list, "g34_parameter_list.csv")


