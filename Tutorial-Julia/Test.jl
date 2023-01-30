module Test
export main

import InteractiveUtils as iutils
import DataStructures as dstructs
mod_patt = r"(Base[.\w\d]*)|in ([.\w\d]*) at"
name_patt = r"^(.*?)\("
method_dict = dstructs.DefaultDict{String, Set{String}}(()->Set{String}())

function main()
    methods = Vector{Method}()
    for type in [AbstractString, String]
        append!(methods, iutils.methodswith(type))
    end
    for (index, method) in enumerate(methods)
        str  = string(method)
        #println(str)
        name = match(name_patt, str)
        if isnothing(name)
            #println(" - No name found")
            push!(method_dict["No Name Match"], str)
            continue
        end
        name = name[1]
        mod  = match(mod_patt, str)
        if isnothing(mod)
            #println(" - No module found")
            push!(method_dict["No Module Match"], str)
            continue
        end
        for grp in mod
            if !isnothing(grp)
                mod = grp
                break
            end
        end
        #println("Matched: $(name) : $(mod)")
        push!(method_dict[mod], name)
        # if index > 100
        #     break
        # end
    end
    lines = Vector{String}()
    for key in sort(collect(keys(method_dict)))
        push!(lines, "\n# " * key)
        for method in sort(collect(method_dict[key]))
            push!(lines, method * "()")
        end
    end
    open("methods.txt", "w") do io
        write(io, join(lines,"\n")*"\n")
    end
    println("$(length(lines)) methods saved to methods.txt")
end

end