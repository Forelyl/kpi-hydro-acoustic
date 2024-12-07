# Base fields for every function

| #     | field name    | type                          |
| :---: | ---           | ---                           |
| 1.    | id:           | unique unsigned int (>= 0)    |
| 1.    | name:         | str (max len: 100)            |
| 2.    | description:  | str (max len: 500)            |
| 3.    | func_type:    | **Options**: Type_list        |
| 4.    | args:         | list[...], ... = Types: Args  |
| 5.    | choose_track: | bool                          |

> choose_track: the value is ***true*** then we select track in drop down menu. ***false*** - when it shouldn't.

let something/someone slide
idiom
Add to word list
to not do anything about something or someone when you should try to change or correct that thing or person:
I knew he wasn’t telling me everything, but I decided to let it slide.
It’s easy to let exercise slide in the suburbs where you have to drive your car all the time.
# Types

### **Args**

| #     | field name   | type                          |
| :---: | ---          | ---                           |
| 1.    | name:        | str (max len: 100)            |
| 2.    | description: | str (max len: 500)            |
| 3.    | datatype:    | **Options**: Datatype         |
| 4.    | units:       | str (max len: 5, min len: 0)  |


# Options

### **Type_list** - str
#### values:
1. Graphical - as a result produces image (no additional tracks).
2. Data modifier - as a result changes some part of the track, yet not producing.additional tracks.
3. Copy - makes n instances of selected track. ()

### **Datatype** - str
#### values:
1. Integer
2. Positive integer - integer that is bigger than zero (> 0)
3. Float
4. Positive float - float that is bigger than zero (> 0.0)
5. Non negative float - float that is bigger than or equals to zero (>= 0.0)
6. Time - is dict of {minutes: a, seconds: b}, a is [0, MAX_FLOAT], b is [0, 60] <br/>
    *example*
    ```ts
    a: Time = {minutes: 12, seconds: 1}; // 12:01
    ```
7. Track - input as list of positive integers <br/>
    *example* <br/>
    ```ts
    a: Track = [2];     // track 2
    b: Track = [2, 3];  // 3-rd copy of track 2
    ```
8. Track characteristics - str, one of three values ["frequency", "amplitude", "time"] <br/>

# Additional/optional fields
Additional/optional fields are such fields which clarify specific base fields or provide additional information.

Optional fields are enabled by corresponding values in base fields or can just be/not be (in this non specific case, has no **value pair that enable**). Corresponding fields should have value of one of **Options** types.

| #     | value pair that enable | field name        | type                          |
| :---: | ---                    | ---               | ---                           |
| 1.    | func_type: Copy        | amount_of_copies: | int (> 0)                     |
| 2.    |                        | args[n].default:  | Any - type of field           |

> Field name is name of field in relation to top level of function. For example amount_of_copies is top level key of function entry

> args[n].default - key **default** is optional key that is located inside any **n-th element** of **args list** that is inside function entry
