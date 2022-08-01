window.onload = function(){
    let r_url = new URL(window.location.href);
    if (r_url.searchParams.get("gender")!=null){
        document.getElementById("gender").value = r_url.searchParams.get("gender")
    }
    if (r_url.searchParams.get("stream")!=null){
        document.getElementById("stream").value = r_url.searchParams.get("stream")
    }
}

function searchFilter(){
    var gender = document.getElementById("gender").value;
    var stream = document.getElementById("stream").value;

    let url = new URL(window.location.href);

    if (gender != "null") {
        url.searchParams.set('gender', gender);
    }  
    if(stream != "null"){
        url.searchParams.set('stream', stream);
    }  
    window.location.href = url; 
}

function showDetailbyID(userid, profile_id, username, catagory){


    $.ajax({
        type: "POST",
        url: "/api/user-details/"+userid+"/?profile_id="+profile_id,
        data: {
            'userid' : userid,
            'profile_id' : profile_id,
            'username' : username,
            'type' : catagory,
            'req_by' : "{{request.user.username}}",
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(msg){
            console.log(msg)
            if (catagory == 't' && msg['status'] == '200'){

                var details_of_rsp = `
                <thead>
                    <tr>
                    <th>Personal Details</th>
                    </tr>
                    <tr>
                        <th>Profile Photo</th>
                        <td> <img style="max-width:120px;" src="/media/${msg['profile'][0]['img']}" alt="" srcset=""> </td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <th> Full Name </th>
                    <td>${msg['profile'][0]['full_name']}</td>
                    </tr>
    
    
                    <tr>
                    <th> Username </th>
                    <td>${msg['account'][0]['username']} </td>
                    <th> Date Joined </th>
                    <td>${msg['account'][0]['date_joined']} </td>
                    </tr>
    
                    <tr>
                    <th> Email </th>
                    <td> ${msg['account'][0]['email']}</td>
                    <th> Gender </th>
                    <td> ${msg['profile'][0]['gender']} </td>
                    </tr>
    
                    <tr>
                    <th>Academic Details</th>
                    </tr>
    
    
                    <tr>
                    <th> Stream </th>
                    <td> ${msg['profile'][0]['stream']} </td>
                    <th> Class Taught </th>
                    <td> ${msg['profile'][0]['classes_taught']} </td>
                    </tr>
    
                    <tr>
                    <th>Contact Details</th>
                    </tr>
    
                    <tr>
                    <th>Contact</th>
                    <td> ${msg['profile'][0]['contact']}</td>
                    </tr>
    
                    <tr>
                    <th>Address</th>
                    <td>${msg['profile'][0]['address']} </td>
                    </tr>
                </tbody>
                `;
            }
            else if(catagory == 's' && msg['status'] == '200'){
                var details_of_rsp = `
                <thead>
                    <tr>
                    <th>Personal Details</th>
                    </tr>
                    <tr>
                        <th>Profile Photo</th>
                        <td> <img style="max-width:120px;" src="/media/${msg['profile'][0]['img']}" alt="" srcset=""> </td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <th> Full Name </th>
                    <td>${msg['profile'][0]['full_name']}</td>
                    </tr>
    
    
                    <tr>
                    <th> Username </th>
                    <td>${msg['account'][0]['username']} </td>
                    <th> Date Joined </th>
                    <td>${msg['account'][0]['date_joined']} </td>
                    </tr>
    
                    <tr>
                    <th> Email </th>
                    <td> ${msg['account'][0]['email']}</td>
                    <th> Gender </th>
                    <td> ${msg['profile'][0]['gender']} </td>
                    </tr>
    
                    <tr>
                    <th>Academic Details</th>
                    </tr>
    
    
                    <tr>
                    <th> Standard </th>
                    <td> ${msg['profile'][0]['standard']} </td>
                    <th> Roll No </th>
                    <td> ${msg['profile'][0]['roll_no']} </td>
                    </tr>

                    <tr>
                        <th> Stream </th>
                        <td> ${msg['profile'][0]['stream']} </td>
                        <th> Section </th>
                        <td> ${msg['profile'][0]['section']} </td>
                    </tr>
    
                    <tr>
                    <th>Contact Details</th>
                    </tr>
    
                    <tr>
                    <th>Contact</th>
                    <td> ${msg['profile'][0]['contact']}</td>
                    </tr>
    
                    <tr>
                    <th>Address</th>
                    <td>${msg['profile'][0]['address']} </td>
                    </tr>
                </tbody>
                `;
            }
            else if(msg['status'] == '200') details_of_rsp=msg['msg']
            else details_of_rsp=''
            document.getElementById("toCompleteDetail").innerHTML = '';
            document.getElementById("toCompleteDetail").innerHTML = details_of_rsp;
        }
    });

    var userdetailDiv = document.getElementById("userdetail");
    userdetailDiv.style.display = 'block';

}

function userdetailDivClose(){
    document.getElementById("userdetail").style.display = 'none'
}
