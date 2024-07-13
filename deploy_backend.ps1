$ErrorActionPreference = "Stop"

try {
    Write-Host "- Start Backend Deploy" -ForegroundColor Green

    # set location to this script dir
    Set-Location $PSScriptRoot

    # aws configure
    $credential = Get-Content "~/credential.yaml" | ConvertFrom-Yaml
    $env:AWS_ACCESS_KEY_ID = $credential.aws.iam.access_key_id
    $env:AWS_SECRET_ACCESS_KEY = $credential.aws.iam.secret_access_key
    $env:AWS_DEFAULT_REGION = $credential.aws.iam.region

    # config
    $deploy_settings = Get-Content "./deploy_settings.yaml" | ConvertFrom-Yaml
    $api_version = $deploy_settings.backend.api_version
    $iam_role_arn = $deploy_settings.backend.iam_role_arn

    # update chalice config file
    $chalice_config_file = "./backend-chalice/.chalice/config.json"
    $config_obj = Get-Content $chalice_config_file | ConvertFrom-Json
    $config_obj.app_name = "back-app-$api_version"
    $config_obj.iam_role_arn = $iam_role_arn
    $config_obj.stages.main.api_gateway_stage = $api_version
    $config_obj | ConvertTo-Json | Out-File $chalice_config_file -Encoding utf8

    Function Check {
        Param($status)
        if (-not $status) {
            throw "- Exeption happend"
        }
    }

    # remove cache file
    Get-ChildItem *.pyc -Recurse | Remove-Item

    # deploy lambda & api gateway
    Set-Location "./backend-chalice"

    Write-Host "- chalice deploy --stage main" -ForegroundColor Yellow
    chalice deploy --stage main
    Check $?

    # create cloudwatch logs group
    $log_group_name = "/aws/lambda/back-app-$api_version-main"
    $log_group = aws logs describe-log-groups --log-group-name-prefix $log_group_name | ConvertFrom-Json
    if ($log_group.logGroups.length -eq 0) {
        Write-Host "- aws logs create-log-group --log-group-name $log_group_name --tags Name=back-app" -ForegroundColor Yellow
        aws logs create-log-group --log-group-name $log_group_name --tags Name=back-app
        Check $?

        Write-Host "- aws logs put-retention-policy --log-group-name $log_group_name --retention-in-days 30" -ForegroundColor Yellow
        aws logs put-retention-policy --log-group-name $log_group_name --retention-in-days 30
        Check $?
    }

    Write-Host "- Successfully Deployed" -ForegroundColor Green

} catch {
    Write-Host $Error[0] -ForegroundColor Red
    Write-Host $PSItem.ScriptStackTrace -ForegroundColor Red

} finally {
    Set-Location $PSScriptRoot
}
