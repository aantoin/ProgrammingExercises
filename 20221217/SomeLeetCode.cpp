class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        //Return the indices of the locations of the target in an ascending list. If not found, return [-1,-1]
        if(nums.size()<1){
            return {-1,-1};
        }

        int search_min = 0;
        int search_max = nums.size();
        
        while(true){
            int search_mid = search_min+(search_max-search_min)/2;
            if(nums[search_mid]<target){
                search_min=search_mid+1;
            }
            else if(nums[search_mid]>target){
                search_max=search_mid;
            }
            else{
                search_min = search_mid-1;
                search_max = search_mid+1;
                while(search_min>=0 && nums[search_min]==target) search_min--;
                while(search_max<nums.size() && nums[search_max]==target) search_max++;
                return {search_min+1,search_max-1};
            }
            if(search_min>=search_max)return {-1,-1};
        }
    }


    int search(vector<int>& nums, int target) {
        //Return the index of the target in the nums array given the non-empty array's items are unique, ascending, and then rotated within the array. Ex: [5,7,8,0,2,3] target 7. Return -1 if not present.
        int search_min = 0;
        int search_max = nums.size();
        while(true){
            int search_mid = search_min + (search_max-search_min)/2;

            if(nums[search_mid]==target)return search_mid;
            //Pull lower search boundary up
            else if(nums[search_mid]>=nums[0] && 
                (target>nums[search_mid] || target<nums[0]) ||
               nums[search_mid]<nums[0] && target<nums[0] && target>nums[search_mid]
            ){
                search_min=search_mid+1;
            }
            //Pull upper search boundary down
            else if(nums[search_mid]<nums[0] && 
                     (target<nums[search_mid] || target>=nums[0]) ||
                    nums[search_mid]>=nums[0] && target>=nums[0] && target<nums[search_mid]
            ){
                search_max=search_mid;
            }

            if(search_min>=search_max)return -1;
        }
    }

    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        //Retrun true if the target is in the matrix of ascending numbers, else false
        if(matrix.size()<1 || matrix[0].size()<1 || matrix[0][0]>target)return false;
        int m = matrix.size();
        int n = matrix[0].size();
        int search_min = 0;
        int search_max = m;
        while(true){
            int search_mid = search_min+(search_max-search_min)/2;
            if(matrix[search_mid][0]==target)return true;
            else if(matrix[search_mid][0]>target)search_max=search_mid;
            else{
                search_min = search_mid;
                if(search_min >= search_max-1){
                    int row = search_mid;
                    search_min=0;
                    search_max=n;
                    while(true){
                        search_mid = search_min+(search_max-search_min)/2;
                        if(matrix[row][search_mid]==target)return true;
                        else if(matrix[row][search_mid]<target)search_min=search_mid+1;
                        else search_max = search_mid;
                        if(search_min>=search_max)return false;
                    }
                }
            }
        }
    }
};