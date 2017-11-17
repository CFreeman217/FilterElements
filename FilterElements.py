import clr
import Autodesk.Revit.DB as DB

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def get_selected_elements():
    """
    Return Selected Elements as a list[]. Returns empty list if no elements are selected.
    Usage:
    - Select 1 or more elements
    > selected_elements = get_selected_elements()
    > []
    """
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(element_id)

    return elements

# Accesses the ID associated with the built-in paramater "System Classification" 
# See RevitApiDocs: BuiltInParameter Enumeration
sysClass_id = DB.ElementId(DB.BuiltInParameter.RBS_SYSTEM_CLASSIFICATION_PARAM)
# The filter needs the ID of the parameter we are searching for:
# See RevitApiDocs: FilterableValueProvider Class
sysClass_prov = DB.ParameterValueProvider(sysClass_id)
# The filter also takes a rule evaluation
# See RevitApiDocs: FilterStringRuleEvaluator Look at the inheritance Heirarchy
# to get an idea of what options this has.
sysClass_rule = DB.FilterStringEquals()
# This line directly translates from the C# example provided in the documentation
# to the python equivalent. See RevitApiDocs: ElementParameterFilter Class
sysClass_filter = DB.FilterStringRule(sysClass_prov, \
                                         sysClass_rule, \
                                         'Domestic Hot Water', \
                                         False)
# Assigns our filter to the element parameter filter so it fits into the 
# 'WherePasses' method
sysClass_param_filter = DB.ElementParameterFilter(sysClass_filter)
# Collect a list of items eligible to get picked by the filter.
# I found OST_PipeCurves from a combination of looking over the built in categories and
col_items = DB.FilteredElementCollector(doc) \
        .OfCategory(DB.BuiltInCategory.OST_PipeCurves) \
        .WherePasses(sysClass_param_filter) \
        .ToElementIds()

selected_elements = get_selected_elements()

cross = set(selected_elements).intersection(col_items)

print("\n" * 2 + "~~ Selected Elements ~~" + "\n" * 2)
for element in selected_elements:
    print(element)

print("\n" * 2 + "~~ Collected Elements ~~" + "\n" * 2)
for item in col_items:
    print(item)

print("\n" * 2 + "~~ Filtered Elements ~~" + "\n" * 2)
for item in cross:
    print(item)

