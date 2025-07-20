so a label is somewhere we jump to 
is there any code that translates the opcodes to high level language? merp


https://en.wikipedia.org/wiki/List_of_CIL_instructions
Manually reversing each opcode using wikipedia

1) load user input 
2) convert user input to character array
3) pop into var0 so var0 -> char array of user input
4) push 32 onto stack 
5) create new array of ints
6) pop into var1 so var1 -> array of ints of size 32
7) ldarg -> bin_array
8) get length called which is 32
9) okay, then go to the label / branch there

label function is a loop, looks like it is iterating through the loop?
label does something like
for i in range(32):
    do label2



label2 function is ???


this chunk of code looks like increment pattern 
			ilgenerator.Emit(OpCodes.Ldloc_3);
			ilgenerator.Emit(OpCodes.Ldc_I4_1);
			ilgenerator.Emit(OpCodes.Add);


looks like there is some add / xor going on but not sure b/t what values
yea i think i can finish this EOD

label4 looks like it's taking the lower byte of something


might be worth the effort to draw out the state diagram for the opcodes as well


# start: 
ilgenerator.Emit(OpCodes.Ldarg_1); // arg1 = user input

// user input to character array
ilgenerator.Emit(OpCodes.Callvirt, typeof(string).GetMethod("ToCharArray", new Type[0]));

// idx[0] = char array
ilgenerator.Emit(OpCodes.Stloc_0);

// push 32 to stack
ilgenerator.Emit(OpCodes.Ldc_I4_S, 32);

// new array of type int of size 32 (consuming previous push)
ilgenerator.Emit(OpCodes.Newarr, typeof(int));

// idx1 = new_arr
ilgenerator.Emit(OpCodes.Stloc_1);

// push user input 
ilgenerator.Emit(OpCodes.Ldarg_1);

// get length and consume item 
ilgenerator.Emit(OpCodes.Callvirt, typeof(string).GetMethod("get_Length", new Type[0]));

// idx2 = 32
ilgenerator.Emit(OpCodes.Stloc_2);

// push 0 onto stack 
ilgenerator.Emit(OpCodes.Ldc_I4_0);

// idx3 = 0
ilgenerator.Emit(OpCodes.Stloc_3);

// go to label
ilgenerator.Emit(OpCodes.Br, label);

# label2:

Summary: this code takes an array and form 0 -> the array, does arr[n] xor arr[n+1]

ilgenerator.MarkLabel(label2);
// push char array 
ilgenerator.Emit(OpCodes.Ldloc_0); 

// push 0 
ilgenerator.Emit(OpCodes.Ldloc_3);

// get array[0] pointer and push, so pointer to first index of the array
ilgenerator.Emit(OpCodes.Ldelema, typeof(char));

// push array0 pointer again 
ilgenerator.Emit(OpCodes.Dup);

// get val at array0, this dereferences so we get array[0]
ilgenerator.Emit(OpCodes.Ldind_U2);

// push chararray
ilgenerator.Emit(OpCodes.Ldloc_0);

// push 0 
ilgenerator.Emit(OpCodes.Ldloc_3);

// push 1
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// increment 
ilgenerator.Emit(OpCodes.Add);

// val at chararray 1
ilgenerator.Emit(OpCodes.Ldelem_U2);

// xor the two values (so in the first run, do arr[0] ^ arr[1])
ilgenerator.Emit(OpCodes.Xor);

// to u2 <-- need to include this truncation step I might be missing after the xor
ilgenerator.Emit(OpCodes.Conv_U2);

// array0 pointer = u2, so arr[0] = arr0 ^ arr1
ilgenerator.Emit(OpCodes.Stind_I2);

// load 0
ilgenerator.Emit(OpCodes.Ldloc_3);

// add 1
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// pop prev, and add
ilgenerator.Emit(OpCodes.Add);

// store loc 3 
ilgenerator.Emit(OpCodes.Stloc_3);

# label: 
ilgenerator.MarkLabel(label);

// load 3, which is 0 
ilgenerator.Emit(OpCodes.Ldloc_3);

// load 2 which is 32
ilgenerator.Emit(OpCodes.Ldloc_2);

// load 1 
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// do 32 - 1 and store 
ilgenerator.Emit(OpCodes.Sub);

// check it is less than, so 0 < (32-1)? if yes, jump to label2
// does this skip the last element? yes it does, because last element is } i think? 
// okay, this makes sense becuase it does arr[n] ^ arr[n+1] so it needs to make sure it doesn't go out of bounds
ilgenerator.Emit(OpCodes.Blt, label2);

// push 32
ilgenerator.Emit(OpCodes.Ldloc_2); 

// push 1
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// push 31 
ilgenerator.Emit(OpCodes.Sub);

// store into idx4 31 
ilgenerator.Emit(OpCodes.Stloc_S, 4);

// jump to label3
ilgenerator.Emit(OpCodes.Br, label3);

python code something like 
for i in range(31):
    arr[i] = arr[i] ^ arr[i+1]

# label4:
ilgenerator.MarkLabel(label4);
// at this point, idx0 = chararray
// idx1 = newarray, idx2 = 32, idx3 = 31 idx4 = 31
// idx4 gets updated

// push idx 1 so new_arr
ilgenerator.Emit(OpCodes.Ldloc_1);     // store into new array / return array

// push idx 2 so push 32 <-- no update
// i dont think idx2 = sz ever gets updated, so it is 32 all the way through
ilgenerator.Emit(OpCodes.Ldloc_2); 

// push 31 <-- this value gets updated, so we need to assign it a variable
ilgenerator.Emit(OpCodes.Ldloc_S, 4);

// 32 - 31 = 1, push 1  
ilgenerator.Emit(OpCodes.Sub);

// push 1
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// push diff-1=0
ilgenerator.Emit(OpCodes.Sub);

// push 31
ilgenerator.Emit(OpCodes.Ldc_I4_S, 31);

// 31 & 0 = 0, push 0    <-- generates the temp value in our code
ilgenerator.Emit(OpCodes.And);

// push array ptr 
ilgenerator.Emit(OpCodes.Ldloc_0);  // take from user specified input

// push idx4 = 31 <-- i
ilgenerator.Emit(OpCodes.Ldloc_S, 4);

// get arr[31]
ilgenerator.Emit(OpCodes.Ldelem_U2);

// push array ptr
ilgenerator.Emit(OpCodes.Ldloc_0); // take from user specified input

// push 31
ilgenerator.Emit(OpCodes.Ldloc_S, 4);

// push 1
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// push 31-1 = 30
ilgenerator.Emit(OpCodes.Sub);

// push 31
ilgenerator.Emit(OpCodes.Ldc_I4_S, 31);

// pop 30, 31 do 30 & 31 = 30 and push
ilgenerator.Emit(OpCodes.And);

// push arr[30]
ilgenerator.Emit(OpCodes.Ldelem_U2);

// and the two values, this creates the sum variable in our code
ilgenerator.Emit(OpCodes.Add);

// idx4 = arr[30] & arr[31]
// where is the store happening?
// storing into new array
// push order is array ptr, index value (bottom -> top)
ilgenerator.Emit(OpCodes.Stelem_I4);

// push 31
ilgenerator.Emit(OpCodes.Ldloc_S, 4);

// push 1
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// idx4 = 31 -1, so idx--;
ilgenerator.Emit(OpCodes.Sub);

// store value / update
ilgenerator.Emit(OpCodes.Stloc_S, 4);

ilgenerator.MarkLabel(label3);

// load idx4, i.e. 31
ilgenerator.Emit(OpCodes.Ldloc_S, 4);

// push 0
ilgenerator.Emit(OpCodes.Ldc_I4_0);

// check greater than or equal to 
ilgenerator.Emit(OpCodes.Bge, label4);

// push 0 
ilgenerator.Emit(OpCodes.Ldc_I4_0);

// store to idx5 = 0 
ilgenerator.Emit(OpCodes.Stloc_S, 5);

// load 0 
ilgenerator.Emit(OpCodes.Ldc_I4_0);

// idx6 = 0 
ilgenerator.Emit(OpCodes.Stloc_S, 6);

// ok, not sure the exact output of this, but it writes to arr1

// jump to 5
// this is just memcmp but still might be good to double check
ilgenerator.Emit(OpCodes.Br, label5);

ilgenerator.MarkLabel(label7);

label 7:
// load new array that we have modified
ilgenerator.Emit(OpCodes.Ldloc_1);

// push 0 
ilgenerator.Emit(OpCodes.Ldloc_S, 6);

// push new_arr [0] 
ilgenerator.Emit(OpCodes.Ldelem_I4);

// push the correct array onto stack 
ilgenerator.Emit(OpCodes.Ldarg_2);

// push 0 
ilgenerator.Emit(OpCodes.Ldloc_S, 6);

// push correct_array [0]
ilgenerator.Emit(OpCodes.Ldelem_I4);

// if not equal, jump to label6
ilgenerator.Emit(OpCodes.Bne_Un, label6);

// push 0 
ilgenerator.Emit(OpCodes.Ldloc_S, 5);

// push 1 
ilgenerator.Emit(OpCodes.Ldc_I4_1);

// push 1=1 + 0
ilgenerator.Emit(OpCodes.Add);

// increment so arg5+=1
ilgenerator.Emit(OpCodes.Stloc_S, 5);


ilgenerator.MarkLabel(label6);
// increment arg6
ilgenerator.Emit(OpCodes.Ldloc_S, 6);
ilgenerator.Emit(OpCodes.Ldc_I4_1);
ilgenerator.Emit(OpCodes.Add);
ilgenerator.Emit(OpCodes.Stloc_S, 6);
ilgenerator.MarkLabel(label5); 
Label 5:
ilgenerator.Emit(OpCodes.Ldloc_S, 6);
ilgenerator.Emit(OpCodes.Ldloc_2);
ilgenerator.Emit(OpCodes.Blt, label7);
ilgenerator.Emit(OpCodes.Ldloc_S, 5);            make sure 5 is the size of the array
ilgenerator.Emit(OpCodes.Ldloc_2);
ilgenerator.Emit(OpCodes.Ceq); Store return value
ilgenerator.Emit(OpCodes.Ret);


Not sure why this isn't working
Need / want to take a look at what I am missing / overlooking in the disassembly

okay, right now i am not understanding why the values are negative, how is that possibru


