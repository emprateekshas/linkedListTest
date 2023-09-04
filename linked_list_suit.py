from emautoapi import *

expect_prompt = "Enter your choice: "

def select_linked_list_op(process, op):
    prompt = read_prompt(process, expect_prompt)
    ip_val = 9999
    if op == 'add':
        ip_val = 1
    elif op == 'deleteElement':
        ip_val = 2 
    elif op == 'deleteFirst':
        ip_val = 3
    elif op == 'deleteLast':
        ip_val = 4        
    elif op == 'display':
        ip_val = 5
    else:
        print("Invalid operation")
    status = provide_inputs(process, ip_val)
    if status != True:
        print("Failed to provide operation")
        return
    return status


def provide_element(process, ex_prompt, ip_val):   
    input_value_prompt = read_prompt(process, ex_prompt)
    if not input_value_prompt in ex_prompt:
        print("Received prompt is not the same as the expected prompt")
        print(f'Expected: {ex_prompt}')
        print(f'Received prompt: {input_value_prompt}')
        return    
    status = provide_inputs(process, ip_val)
    
    if status != True:
        print("Failed to provide element")
        return 


def display_data(process,read_length = None):
    data = ''
    if read_length == None:
        data = read_text_output(process)
    else:  
        data = process.stdout.read(read_length).strip() 
    return data      


def get_output_dictionary(process):    
    template_file = "/home/prateeksha/linkedList/linkedListTest/template/linked_list_test.tmpl"
    result = read_dict_output(process, template_file)
    return result     


def match_list(result, expected_output):

    if len(result) == 0:
        return False
    
    if result[0]["result"].strip() in expected_output.strip():
        return True
    else:
        return False


def test_case_1_delete_from_empty(process):
    tc_io_map = {"expected_output": "List Element Count: 0"}
    #TC_banner(reason = "started")
    TC_banner(1, "Delete from empty list", "STARTED")
    #print("Testing for deleting from empty list\n")
    print("Prerequisite: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    print("Delete from empty list")
    select_linked_list_op(process, op = "deleteLast")
    data = display_data(process)
    print(data)

    select_linked_list_op(process, op = "display")
    result = get_output_dictionary(process)
    status = match_list(result, tc_io_map['expected_output'])
    #print("status",status)
    TC_banner(1, "Delete from empty list","PASSED" if status == True else "FAILED")



def test_case_2_add_to_empty(process):
    tc_io_map = {"expected_output": "List Element Count: 1\nList Elements: 5"}
    exp_op = tc_io_map["expected_output"]
    TC_banner(2, "Add element to empty list", reason = "STARTED")
    #print("\nTesting for adding to empty list\n")
    print("Prerequisite: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    print("Element 5 added to the empty list")
    select_linked_list_op(process, op = "add")
    ex_prompt = "Enter the element to be added: "
    provide_element(process, ex_prompt, ip_val = 5)
    data = display_data(process)
    print(data)

    print("Display the list: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    select_linked_list_op(process, op = "display")
    result = get_output_dictionary(process)
    #c_result = {'result': '\n'.join([item['result'] for item in result])}
    #print(c_result)
    
    status = match_list(result, tc_io_map['expected_output'])
    TC_banner(2, "Add element to empty list", "PASSED" if status == True else "FAILED")
    

def test_case_3_add_to_list_having_1_ele(process):
    tc_io_map = {"expected_output": "List Element Count: 2\nList Elements: 5, 8"}
    exp_op = tc_io_map["expected_output"]
    TC_banner(3, "Add element to already existing list", reason = "STARTED")
    #print("\nTesting for adding to already existing list")
    print("Prerequisite: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    print("Add element 8 to list having element 5") 
    select_linked_list_op(process, op = "add")
    ex_prompt = "Enter the element to be added: "
    provide_element(process, ex_prompt, ip_val = 8)
    data = display_data(process)
    print(data)

    print("Display the list: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    select_linked_list_op(process, op = "display")
    result = get_output_dictionary(process)

    status = match_list(result, tc_io_map['expected_output']) 
    TC_banner(3, "Add element to already existing list","PASSED" if status == True else "FAILED")


def test_case_4_add_n_ele_delete_2_ele(process):
    tc_io_map = {"expected_output": "List Element Count: 3\nList Elements: 7, 8, 9"}
    exp_op = tc_io_map["expected_output"]
    TC_banner(4, "Add n elements and delete m elements", reason = "STARTED")
    print("Prerequisite: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    print("Add 3 elements ")
    select_linked_list_op(process, op = "add")
    ex_prompt = "Enter the element to be added: "
    provide_element(process, ex_prompt, ip_val = 6)
    select_linked_list_op(process, op = "add")
    provide_element(process, ex_prompt, ip_val = 7)
    select_linked_list_op(process, op = "add")
    provide_element(process, ex_prompt, ip_val = 9)

    print("Display the list: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)


    select_linked_list_op(process, op = "deleteElement")
    ex_prompt = "Enter the element you want to delete: "
    print("Delete element 6 from list")
    provide_element(process, ex_prompt, ip_val = 6)
    print("Display the list: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    print("Delete first element from the list")
    select_linked_list_op(process, op = "deleteFirst")
    print("Display the list: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    select_linked_list_op(process, op = "display")
    result = get_output_dictionary(process)
    status = match_list(result, tc_io_map['expected_output'])
    TC_banner(4, "Add n elements and delete m elements","PASSED" if status == True else "FAILED")
    

def test_case_5_delete_ele_not_present(process):
    tc_io_map = {"expected_output": "List Element Count: 3\nList Elements: 7, 8, 9"}
    exp_op = tc_io_map["expected_output"]
    TC_banner(5, "Delete an element not present in the list", reason = "STARTED")
    print("Prerequisite Condition:")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    print("Delete element 10 not present in the list")
    select_linked_list_op(process, op = "deleteElement")
    ex_prompt = "Enter the element you want to delete:"
    provide_element(process, ex_prompt, ip_val = 10) 
    data = display_data(process)
    print(data)

    print("Displaying the list: ")
    select_linked_list_op(process, op = "display")
    data = display_data(process)
    print(data)

    select_linked_list_op(process, op = "display")
    result = get_output_dictionary(process)
    status = match_list(result, tc_io_map['expected_output'])  
    TC_banner(5, "Delete an element not present in the list","PASSED" if status == True else "FAILED")  
 


def linked_list_test_main():
    prgm_src_file = "/home/prateeksha/linkedList/linkedListTest/linked_list.c"
    prgm_exec_file ="/home/prateeksha/linkedList/linkedListTest/linked_list"

    status, exec_file = compile_program(prgm_src_file, prgm_exec_file)
    #if status != True:
    if status == False:
        return

    process = run_program(exec_file)
    if process == None:
        return

    #enable_emautoapi_debug()  

    test_case_1_delete_from_empty(process)

    test_case_2_add_to_empty(process)

    test_case_3_add_to_list_having_1_ele(process)

    test_case_4_add_n_ele_delete_2_ele(process)

    test_case_5_delete_ele_not_present(process)

 

if __name__ == "__main__":    
    linked_list_test_main()
