import TableExtractor as te
import TableLinesDetector as tld


path_to_image = "D:\\University\\YEAR 04 SEM 02\\CGV\\Assignment\\image-processing-model\\src\\uploads\\2.jpeg"
table_extractor = te.TableExtractor(path_to_image)
perspective_corrected_image = table_extractor.execute()

table_lines_remover = tld.TableLinesDetector(perspective_corrected_image)
table_lines_remover.execute()


