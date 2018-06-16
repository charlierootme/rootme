import angr
ignored_functions = [ "__errno_location", "strerror", "__gmon_start__","realloc", "__libc_start_main", "printf", "fprintf", "malloc"] 

avoid=0x804871e
find=[0x08048709,0x0804871c]
main = 0x804869d
input_addr = 0

p = angr.project.Project("ch1.bin", ignore_functions=ignored_functions, load_options={"auto_load_libs":False}, use_sim_procedures=True )

es = p.factory.entry_state(addr = main, concrete_fs=False)
es.mem[es.regs.ebp - 0xc].dword = input_addr
input_bvs = es.se.BVS("input", 0x10*8)
es.memory.store(input_addr, input_bvs )
sm = p.factory.simulation_manager(es)
print("Exploring...")
test = sm.explore(find=find, avoid=avoid)
print("Done !")
for f in test.found:
    resp = f.state.se.eval(input_bvs,cast_to=str)
    print("Response is {}\nIn Hex : {}".format(resp, resp.encode("hex")))
