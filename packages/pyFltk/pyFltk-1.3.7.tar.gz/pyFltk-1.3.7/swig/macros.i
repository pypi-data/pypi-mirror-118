// macro to delegate the ownership of a class to C++
%define CHANGE_OWNERSHIP(name)
%pythonappend name##::##name %{
if len(args) == 5:          
    # retain reference to label
    self.my_label = args[-1]
if self.parent() != None:   
    # delegate ownership to C++
    self.this.disown()
%}
%enddef

// macro to revert the ownership
%define REVERT_OWNERSHIP(name)
%pythonappend name %{
#self = args[0]
if self.parent() != None:   
    #delegate ownership to C++
    self.this.disown()
else:                       
    #give ownership back to Python
    self.this.own() 
%}
%enddef

