import TableExtractor as te


path_to_image = "D:\\University\\YEAR 04 SEM 02\\CGV\\Assignment\\image-processing-model\\src\\uploads\\2.jpeg"
table_extractor = te.TableExtractor(path_to_image)
table_extractor.execute()