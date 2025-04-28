resource "azurerm_storage_account" "storage" {
  name                     = "khoitruongstorageaccount"   # must be globally unique
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "dev"
  }
}

#Blob container
resource "azurerm_storage_container" "container" {
  name                  = "testcontainer"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private" # private, blob, or container
}

#Grant permisson
resource "azurerm_role_assignment" "blob_contributor" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = "b2d35218-2d31-4d95-a0b7-1d4755f1b37d"  # User, SP, or Managed Identity ID
}

output "data_storage_id" {
  value = azurerm_storage_account.storage.name
}


