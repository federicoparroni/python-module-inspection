import pkgutil
import importlib, inspect

def get_modules_in_pkg(pkg_path):
    return [(name, ispkg) for _, name, ispkg in pkgutil.iter_modules([pkg_path])]

def gather_classes(pkg, subclass_of=None):
    schema_classes = []

    package = importlib.import_module(pkg)
    modules = get_modules_in_pkg(package.__path__[0])
    for module, ispkg in modules:
        modname = f'{pkg}.{module}'
        
        imported_module = importlib.import_module(modname)
        classes = inspect.getmembers(imported_module, inspect.isclass)
        for class_name, class_obj in classes:
            if subclass_of is not None:
                if class_obj is subclass_of:
                    continue
                if not issubclass(class_obj, subclass_of):
                    continue
            schema_classes.append(class_obj)
        if ispkg:
            # recursively get from subpkg
            schema_classes.extend(gather_classes(modname, subclass_of))
    return schema_classes


if __name__ == '__main__':
    from test import Test
    
    classes = gather_classes('test.mymodule', subclass_of=Test)
    for cls in classes:
        print(str(cls))